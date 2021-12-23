'''
Function:
    根据IP地址查询地理信息小工具
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

    
'''根据IP地址查询地理信息小工具'''
class IPLocationQuery():
    tool_name = '根据IP地址查询地理信息小工具'
    def __init__(self, ipaddress='202.108.23.153', **kwargs):
        self.ipaddress = ipaddress
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        }
    '''运行'''
    def run(self):
        separator = '*' * 30 + 'IPLocQuery' + '*' * 30
        if self.isIP(self.ipaddress):
            print(separator)
            print(self.getTaobaoIP(self.ipaddress))
            print(self.getIpstackIP(self.ipaddress))
            print(self.getIpapiIP(self.ipaddress))
            print('*' * len(separator))
        else:
            print(separator + '\n[Error]: %s --> 无效IP地址...\n' % self.ipaddress + '*' * len(separator))
    '''IP地址有效性验证'''
    def isIP(self, ip):
        try:
            IPy.IP(ip)
            return True
        except:
            return False
    '''淘宝API'''
    def getTaobaoIP(self, ip):
        url = 'https://ip.taobao.com/outGetIpInfo'
        response = requests.post(url, data={'ip': ip, 'accessKey': 'alibaba-inc'})
        data = response.json().get('data')
        if data is None:
            return '[淘宝API查询结果-IP]: %s\n无效IP' % ip
        result = '-' * 50 + '\n' + \
        '''[淘宝API查询结果-IP]: %s\n国家: %s\n地区: %s\n城市: %s\n''' % (ip, data.get('country'), data.get('region'), data.get('city')) \
        + '-' * 50
        return result
    '''ipstack.com'''
    def getIpstackIP(self, ip):
        url = 'http://api.ipstack.com/{}?access_key=19e7f2b6fe27deb566140aae134dec6b'
        response = requests.get(url.format(ip), headers=self.headers)
        data = response.json()
        continent_name = data.get('continent_name')
        country_name = data.get('country_name')
        region_name = data.get('region_name')
        city = data.get('city')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        result = '-' * 50 + '\n' + \
        '''[ipstack.com查询结果-IP]: %s\n经纬度: (%s, %s)\n板块: %s\n国家: %s\n地区: %s\n城市: %s\n''' % (ip, longitude, latitude, continent_name, country_name, region_name, city) \
        + '-' * 50
        return result
    '''ip-api.com(很不准)'''
    def getIpapiIP(self, ip):
        url = 'http://ip-api.com/json/'
        response = requests.get(url+ip, headers=self.headers)
        data = response.json()
        city = data.get('city')
        country = data.get('country')
        region_name = data.get('regionName')
        latitude = data.get('lat')
        longitude = data.get('lon')
        result = '-' * 50 + '\n' + \
        '''[ip-api.com查询结果-IP]: %s\n经纬度: (%s, %s)\n国家: %s\n地区: %s\n城市: %s\n''' % (ip, longitude, latitude, country, region_name, city) \
        + '-' * 50
        return result