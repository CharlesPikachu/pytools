'''
Function:
    国内访问Github一键加速脚本
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import re
import shutil
import requests
import platform
from tqdm import tqdm
from pythonping import ping
from bs4 import BeautifulSoup


'''国内访问Github一键加速脚本'''
class GithubAcceleration():
    tool_name = '国内访问Github一键加速脚本'
    def __init__(self, domains=None, hosts_path=None, proxies={'https': '127.0.0.1:1080'}):
        self.domains = [
            'github.com', 'www.github.com', 'github.global.ssl.fastly.net', 'github.map.fastly.net', 'github.githubassets.com',
            'github.io', 'assets-cdn.github.com', 'gist.github.com', 'help.github.com', 'api.github.com', 'nodeload.github.com',
            'codeload.github.com', 'raw.github.com', 'documentcloud.github.com', 'status.github.com', 'training.github.com',
            'raw.githubusercontent.com', 'gist.githubusercontent.com', 'cloud.githubusercontent.com', 'camo.githubusercontent.com',
            'avatars0.githubusercontent.com', 'avatars1.githubusercontent.com', 'avatars2.githubusercontent.com', 'avatars3.githubusercontent.com',
            'avatars4.githubusercontent.com', 'avatars5.githubusercontent.com', 'avatars6.githubusercontent.com', 'avatars7.githubusercontent.com',
            'avatars8.githubusercontent.com', 'user-images.githubusercontent.com', 'favicons.githubusercontent.com', 'github-cloud.s3.amazonaws.com',
            'github-production-release-asset-2e65be.s3.amazonaws.com', 'github-production-user-asset-6210df.s3.amazonaws.com',
            'github-production-repository-file-5c1aeb.s3.amazonaws.com', 'alive.github.com', 'guides.github.com', 'docs.github.com'
        ] if domains is None else domains
        self.hosts_path = hosts_path
        if self.hosts_path is None:
            if 'Windows' in platform.platform():
                self.hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
            else:
                self.hosts_path = '/etc/hosts'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36'
        }
        self.session = requests.Session()
        if proxies is not None: self.session.proxies.update(proxies)
        self.session.headers.update(self.headers)
    '''运行'''
    def run(self):
        domain2ip_dict = {}
        # 生成符合ipadredd.com查询的url地址, 从而解析出域名对应的IP
        pbar = tqdm(self.domains)
        for domain in pbar:
            pbar.set_description(f'parse {domain}')
            url = f'https://ipaddress.com/website/{domain}'
            response = self.session.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'lxml')
            ips = []
            for item in soup.find('tbody', id='dnsinfo').select('tr td a'):
                ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", item.text)
                if ip: ips.append(''.join(ip))
            assert len(ips) > 0, f'parse {domain} error'
            if len(ips) == 1:
                domain2ip_dict[domain] = ''.join(ips)
            else:
                domain2ip_dict[domain] = self.lowestrttip(ips)
        # 更新host文件
        print(f'[INFO]: start to update the host file')
        shutil.copy(self.hosts_path, self.hosts_path + '.bak')
        fp_host, fp_temp = open(self.hosts_path, 'r'), open('temphost', 'w')
        def distinct(domains, line):
            for domain in domains:
                if domain in line: return True
            return False
        for line in fp_host.readlines():
            if not distinct(self.domains, line):
                fp_temp.write(line)
        for domain, ip in domain2ip_dict.items():
            fp_temp.write(f'{ip}\t{domain}\n')
        fp_host.close()
        fp_temp.close()
        shutil.copy('./temphost', self.hosts_path)
        os.remove('./temphost')
        if 'Windows' in platform.platform():
            os.system('ipconfig /flushdns')
        else:
            os.system('systemd-resolve --flush-caches')
        print(f'[INFO]: update the host file successfully')
    '''ping所有的ip并返回TTS最小的ip'''
    def lowestrttip(self, ips):
        best_ip, best_ip_tts = None, 1e10
        for ip in ips:
            result = ping(ip, timeout=1, count=5, verbose=False)
            avg_tts = result.rtt_avg
            if best_ip_tts > avg_tts:
                best_ip_tts, best_ip = avg_tts, ip
        return best_ip