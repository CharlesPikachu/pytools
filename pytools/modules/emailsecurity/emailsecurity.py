'''
Function:
    邮箱安全性验证工具
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import re
import time
import random
import hashlib
import requests
from lxml import etree


'''邮箱安全性验证工具'''
class EmailSecurity():
    tool_name = '邮箱安全性验证工具'
    def __init__(self, emails=None, check_mode='Haveibeenpwned', hibp_api_key=None, **kwargs):
        assert check_mode in ['Firefox', 'Haveibeenpwned']
        if hibp_api_key is None: hibp_api_key = random.choice(['e0c4c2b5c7304030912b2251e15d7dac', '398bba8c95cc4db4a23138af3037a496', 'f269230d7044457a910dc8d2d1205013'])
        if emails is None:
            emails = [
                'stevenlmh@163.com', 'hubeiyangyi@163.com', 'h465932675@163.com', 'xiajiahao456@163.com', 
                'zhangaorui1@163.com', 'babby126@163.com', 'a794685816@163.com', 'zzw67090@163.com',
                'maye915@163.com', 'mao164951618@163.com', 'mczhoulei2011@163.com'
            ]
        self.emails = emails
        self.check_mode = check_mode
        self.hibp_api_key = hibp_api_key
    '''运行'''
    def run(self):
        if 'Firefox' == self.check_mode:
            return self.checkFirefox(self.emails)
        elif 'Haveibeenpwned' == self.check_mode:
            return self.checkHaveibeenpwned(self.emails)
    '''使用https://monitor.firefox.com/验证'''
    def checkFirefox(self, emails):
        print('[INFO]: Using https://monitor.firefox.com/ to verify the security of your email...')
        url = 'https://monitor.firefox.com/scan'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        session = requests.Session()
        response = session.get(url, headers=headers)
        csrf = re.findall(r'name="_csrf" value="(.*?)"', response.text)[0]
        print('[Results]:')
        results = {}
        for idx, email in enumerate(emails):
            sha1 = hashlib.sha1()
            sha1.update(email.encode('utf-8'))
            email_sha1 = sha1.hexdigest()
            data = {
                'emailHash': email_sha1,
                'pageToken': '',
                'email': '',
                '_csrf': csrf,
            }
            response = session.post(url, headers=headers, data=data)
            html = etree.HTML(response.text)
            info = html.xpath('string(/html/body/main/div[1]/div/h2)')
            if int(re.findall(r'此电子邮件地址出现在(.*?)次已知数据外泄事件中', info)[0]) > 0:
                info += html.xpath('string(/html/body/main/div[2]/div[1]/a/div[2]/div[1])')
            result = info.replace(' ', '').replace('\n', '')
            results[email] = result
            print('----[%d]: %s → %s' % (idx+1, email, result))
            if idx+1 != len(email): time.sleep(1 + random.random() * 2)
        return results
    '''使用https://haveibeenpwned.com/验证'''
    def checkHaveibeenpwned(self, emails):
        print('[INFO]: Using https://haveibeenpwned.com/ to verify the security of your email...')
        url = 'https://haveibeenpwned.com/api/v3/breachedaccount/{}'
        headers = {'hibp-api-key': self.hibp_api_key}
        session = requests.Session()
        print('[Results]:')
        results = {}
        for idx, email in enumerate(emails):
            response = session.get(url.format(email), verify=True, headers=headers)
            if response.status_code == 200:
                result = '存在泄露, 详情如下:\n'
                for leak in response.json():
                    info = session.get(f'https://haveibeenpwned.com/api/v3/breach/{leak["Name"]}').json()
                    for key, value in info.items():
                        result += f'{key}: {value}; '
            elif response.status_code == 404:
                result = '账号安全, 无泄露记录.'
            elif response.status_code == '429':
                result = '验证过于频繁, 请%s秒后重试.' % str(response.headers['Retry-After'])
            else:
                result = '验证过程中出现未知错误, 请尝试重新运行程序.'
            results[email] = result
            print('----[%d]: %s → %s' % (idx+1, email, result))
            if idx+1 != len(email): time.sleep(1 + random.random() * 2)
        return results
    

