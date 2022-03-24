'''
Function:
    每天从arxiv获取自己感兴趣的论文
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import time
import click
import random
import pickle
import requests
from bs4 import BeautifulSoup


'''每天从arxiv获取自己感兴趣的论文'''
class ArxivHelper():
    tool_name = 'Arxiv小助手'
    def __init__(self, keywords_list=['continual learning'], history_filename='cache.pkl', time_interval=3600*5, server_key=None, **kwargs):
        self.history_filename = history_filename
        self.keywords_list = keywords_list
        self.time_interval = time_interval
        self.server_key = server_key
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        }
    '''运行'''
    def run(self):
        while True:
            print('*' * 50)
            # 获得所有相关文章信息
            all_results = {}
            for keyword in self.keywords_list:
                try:
                    results = self.search(keyword)
                    all_results.update(results)
                except Exception as err:
                    self.logging(err)
                time.sleep(5 + random.random())
            all_results = self.readhistoryandfilter(all_results)
            self.logging(f'搜索完成, 共获得{len(all_results)}相关的最新论文')
            # 发送Server酱提示
            self.pushwechat(all_results)
            self.logging(f'发送微信看论文提示成功')
            # 下载所有论文
            dirname, download_papers = str(int(time.time())), []
            self.touch(dirname)
            for url, result in all_results.items():
                savepath = os.path.join(dirname, result['title']+'.pdf')
                try:
                    self.download(url, savepath)
                    download_papers.append(url)
                except Exception as err:
                    self.logging(err)
            self.logging(f'下载完成, 共下载{len(download_papers)}相关的最新论文')
            self.logging(f'将在{self.time_interval}秒后再次从arxiv搜索并下载相关内容')
            # sleep
            time.sleep(self.time_interval)
            print('*' * 50 + '\n' * 3)
    '''下载pdf'''
    def download(self, url=None, savepath='tmp.pdf'):
        url = url.replace('abs', 'pdf') + '.pdf'
        try:
            is_success = False
            with self.session.get(url, stream=True) as response:
                if response.status_code == 200:
                    total_size, chunk_size = int(response.headers['content-length']), 1024
                    label = '[FileSize]: %0.2fMB' % (total_size / 1024 / 1024)
                    with click.progressbar(length=total_size, label=label) as progressbar:
                        with open(savepath, 'wb') as fp:
                            for chunk in response.iter_content(chunk_size=chunk_size):
                                if chunk:
                                    fp.write(chunk)
                                    progressbar.update(len(chunk))
                    is_success = True
        except:
            is_success = False
        return is_success
    '''发送Server酱提示'''
    def pushwechat(self, all_results):
        server_url = f'https://sc.ftqq.com/{self.server_key}.send'
        desp = []
        for url, result in all_results.items():
            text = f'标题: {result["title"]}\n\n作者: {result["authors"]}\n\n摘要: {result["abstract"]}'
            desp.append(text)
        data = {
            'text': f'又有{len(all_results)}篇你感兴趣的论文在arxiv上发布啦!',
            'desp': '\n\n\n\n\n\n\n\n'.join(desp),
        }
        response = requests.post(server_url, data=data)
        return response
    '''打印日志'''
    def logging(self, text):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} INFO]: {text}')
    '''新建文件夹'''
    def touch(self, dirname):
        if not os.path.exists(dirname):
            os.mkdir(dirname)
            return False
        return True
    '''搜索'''
    def search(self, keyword):
        # 请求arxiv cs相关的搜索API
        keyword = keyword.replace(' ', '+')
        url = 'https://arxiv.org/search/cs?'
        params = {
            'query': keyword,
            'searchtype': 'all',
            'abstracts': 'show',
            'order': '-announced_date_first',
            'size': '50',
        }
        response = self.session.get(url, params=params)
        # 解析返回的结果
        soup = BeautifulSoup(response.text, features='lxml')
        results = {}
        for item in soup.find('ol').find_all('li', attrs={'class': 'arxiv-result'}):
            try: title = item.find('p', attrs={'class': 'title'}).text.strip()
            except: title = ''
            try: authors = self.cleantext(item.find('p', attrs={'class': 'authors'}).text.strip()).replace('Authors:', '')
            except: authors = ''
            try: abstract = self.cleantext(item.find('p', attrs={'class': 'abstract'}).text.strip()).replace('Abstract:', '')
            except: abstract = ''
            try: comments = self.cleantext(item.find('p', attrs={'class': 'comments'}).text.strip()).replace('Comments:', '')
            except: comments = ''
            try: url = item.find('p', attrs={'class': 'list-title'}).find('a').attrs['href']
            except: url = ''
            if not url: continue
            result = {
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'comments': comments,
                'url': url,
            }
            results[result['url']] = result
        return results
    '''清理文本'''
    def cleantext(self, text):
        text = text.replace('\n', '')
        text, text_clean = text.split(' '), []
        for item in text:
            if item: text_clean.append(item)
        text = ' '.join(text_clean)
        return text
    '''读取历史发送的内容并过滤已经发送过的内容'''
    def readhistoryandfilter(self, results):
        # 读取
        if os.path.isfile(self.history_filename):
            fp = open(self.history_filename, 'rb')
            history = pickle.load(fp)
            fp.close()
        else:
            history = []
        # 去重
        urls = list(results.keys())
        for url in urls:
            if url in history:
                results.pop(url)
            else:
                history.append(url)
        # 保存
        fp = open(self.history_filename, 'wb')
        pickle.dump(history, fp)
        fp.close()
        # 返回
        return results