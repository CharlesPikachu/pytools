'''
Function:
	邮箱安全性验证V1.0
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import sys
import time
import random
import hashlib
import requests
import cfscrape
import argparse
from lxml import etree


'''使用https://monitor.firefox.com/验证'''
def checkFirefox(emails):
	print('[INFO]: Using https://monitor.firefox.com/ to verify the security of your email...')
	url = 'https://monitor.firefox.com/scan'
	headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
				'Accept-Language': "zh-CN,zh;q=0.9"
			}
	print('[Results]:')
	results = []
	for idx, email in enumerate(emails):
		sha1 = hashlib.sha1()
		sha1.update(email.encode('utf-8'))
		email_sha1 = sha1.hexdigest()
		data = {
					'emailHash': email_sha1
				}
		res = requests.post(url, headers=headers, data=data)
		html = etree.HTML(res.text)
		info_len = len(html.xpath('//section[@id="download-firefox"]/div/div'))
		info = ''
		for i in range(info_len):
			info += html.xpath('string(//main[@class="scan-results"]/div/section[@class="half"][%s])' % (i+1))
		result = info.replace(' ', '').replace('\n', '')
		results.append([email, result])
		print('--[%d]: %s → %s' % (idx+1, email, result))
		time.sleep(1 + random.random() * 2)
	return results


'''使用https://haveibeenpwned.com/验证'''
def checkHaveibeenpwned(emails):
	print('[INFO]: Using https://haveibeenpwned.com/ to verify the security of your email...')
	url = 'https://haveibeenpwned.com/api/breachedaccount/{}'
	pasteaccount_url = 'https://haveibeenpwned.com/api/v2/pasteaccount/{}'
	headers = {
				'User-Agent': 'PwnChecker-API-Python-Script'
			}
	cookies, user_agent = cfscrape.get_tokens("https://haveibeenpwned.com/api/breachedaccount/test@example.com", user_agent=headers.get('User-Agent'))
	print('[Results]:')
	results = []
	for idx, email in enumerate(emails):
		res = requests.get(url.format(email), headers=headers, cookies=cookies, verify=True)
		if str(res.status_code) == '404':
			result = '账号安全, 无违规记录.'
		elif str(res.status_code) == '200':
			result = '账号存在风险, 有违规记录, 请及时修改密码.详情如下:\n'
			res = requests.get(pasteaccount_url.format(email), headers=headers, cookies=cookies, verify=True)
			if str(res.status_code) == '200':
				json_data = json.dumps(res.content)
				for key, value in json_data.items():
					result += str(key) + ':' + str(value) + ';'
			else:
				result += '详情获取失败QAQ...'
		elif str(res.status_code) == '429':
			raise RuntimeError('验证过于频繁, 请%s秒后重试...' % str(res.headers['Retry-After']))
		elif str(res.status_code) == '503':
			raise RuntimeError('请求被CloudFlare终止, 请确保你使用的ua和cookie是正确的...')
		else:
			raise RuntimeError('验证过程中出现未知错误, 请尝试重新运行程序...')
		results.append([email, result])
		print('--[%d]: %s → %s' % (idx+1, email, result))
		time.sleep(1 + random.random() * 2)
	return results
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Used to verify the security of your email addresses.")
	parser.add_argument('-f', dest='filename', help='File to be checked with one email address per line')
	parser.add_argument('-e', dest='email', help='Single email address to be checked')
	args = parser.parse_args()
	email = args.email
	emailfile = args.filename
	if email:
		checkFirefox([email])
		checkHaveibeenpwned([email])
	if emailfile:
		emails = [email.strip('\n') for email in open(emailfile)]
		checkFirefox(emails)
		checkHaveibeenpwned(emails)