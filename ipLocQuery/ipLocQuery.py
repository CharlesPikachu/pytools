'''
Function:
	根据IP地址查其对应的地理信息
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import IPy
import time
import random
import hashlib
import argparse
import requests


headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


'''淘宝API'''
def getTaobaoIP(ip):
	url = 'http://ip.taobao.com/service/getIpInfo.php?ip='
	res = requests.get(url+ip, headers=headers)
	data = res.json().get('data')
	if data is None:
		return '[淘宝API查询结果-IP]: %s\n无效IP' % ip
	result = '-'*50 + '\n' + \
	'''[淘宝API查询结果-IP]: %s\n国家: %s\n地区: %s\n城市: %s\n''' % (ip, data.get('country'), data.get('region'), data.get('city')) \
	+ '-'*50
	return result


'''ip-api.com(很不准)'''
def getIpapiIP(ip):
	url = 'http://ip-api.com/json/'
	res = requests.get(url+ip, headers=headers)
	data = res.json()
	yd = youdao()
	city = yd.translate(data.get('city'))[0]
	country = yd.translate(data.get('country'))[0]
	region_name = yd.translate(data.get('regionName'))[0]
	latitude = data.get('lat')
	longitude = data.get('lon')
	result = '-'*50 + '\n' + \
	'''[ip-api.com查询结果-IP]: %s\n经纬度: (%s, %s)\n国家: %s\n地区: %s\n城市: %s\n''' % (ip, longitude, latitude, country, region_name, city) \
	+ '-'*50
	return result


'''ipstack.com'''
def getIpstackIP(ip):
	url = 'http://api.ipstack.com/{}?access_key=1bdea4d0bf1c3bf35c4ba9456a357ce3'
	res = requests.get(url.format(ip), headers=headers)
	data = res.json()
	yd = youdao()
	continent_name = yd.translate(data.get('continent_name'))[0]
	country_name = yd.translate(data.get('country_name'))[0]
	region_name = yd.translate(data.get('region_name'))[0]
	city = yd.translate(data.get('city'))[0]
	latitude = data.get('latitude')
	longitude = data.get('longitude')
	result = '-'*50 + '\n' + \
	'''[ipstack.com查询结果-IP]: %s\n经纬度: (%s, %s)\n板块: %s\n国家: %s\n地区: %s\n城市: %s\n''' % (ip, longitude, latitude, continent_name, country_name, region_name, city) \
	+ '-'*50
	return result


'''IP地址有效性验证'''
def isIP(ip):
	try:
		IPy.IP(ip)
		return True
	except:
		return False


'''
Function:
	有道翻译类
'''
class youdao():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
						'Referer': 'http://fanyi.youdao.com/',
						'Cookie': 'OUTFOX_SEARCH_USER_ID=-481680322@10.169.0.83;'
					}
		self.data = {
						'i': None,
						'client': 'fanyideskweb',
						'keyfrom': 'fanyi.web',
						'salt': None,
						'sign': None
					}
		self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
	def translate(self, word):
		if word is None:
			return [word]
		t = str(time.time()*1000 + random.randint(1, 10))
		self.data['i'] = word
		self.data['salt'] = t
		sign = 'fanyideskweb' + word + t + '6x(ZHw]mwzX#u0V7@yfwK'
		self.data['sign'] = hashlib.md5(sign.encode('utf-8')).hexdigest()
		res = requests.post(self.url, headers=self.headers, data=self.data)
		return res.json()['translateResult']


'''主函数'''
def main(ip):
	separator = '*' * 30 + 'IPLocQuery' + '*' * 30
	if isIP(ip):
		print(separator)
		print(getTaobaoIP(ip))
		print(getIpstackIP(ip))
		print(getIpapiIP(ip))
		print('*' * len(separator))
	else:
		print(separator + '\n[Error]: %s --> 无效IP地址...\n' % ip + '*' * len(separator))
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Query geographic information based on IP address.")
	parser.add_argument('-f', dest='filename', help='File to be queried with one ip address per line')
	parser.add_argument('-ip', dest='ipaddress', help='Single ip address to be queried')
	args = parser.parse_args()
	ip = args.ipaddress
	filename = args.filename
	if ip:
		main(ip)
	if filename:
		with open(filename) as f:
			ips = [ip.strip('\n') for ip in f.readlines()]
		for ip in ips:
			main(ip)
