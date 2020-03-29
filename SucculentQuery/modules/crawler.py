'''
Function:
    多肉数据爬虫
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import time
import random
import pickle
import requests
from lxml import etree


'''多肉数据爬虫'''
class SucculentCrawler():
    def __init__(self, **kwargs):
        self.referer_list = ["http://www.google.com/", "http://www.bing.com/", "http://www.baidu.com/", "https://www.360.cn/"]
        self.ua_list = ['Mozilla/5.0 (Linux; Android 5.1.1; Z828 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.111 Mobile Safari/537.36',
                        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22',
                        'Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/47.0.2526.107 Mobile/12F69 Safari/600.1.4',
                        'Mozilla/5.0 (iPad; CPU OS 11_2_5 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) CriOS/64.0.3282.112 Mobile/15D60 Safari/604.1',
                        'Mozilla/5.0 (Linux; Android 7.1.1; SM-T350 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Safari/537.36',
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Safari/537.36',
                        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36',
                        'Mozilla/5.0 (Linux; Android 6.0.1; SM-G610F Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                        'Mozilla/5.0 (Linux; Android 5.1.1; 5065N Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/46.0.2490.76 Mobile Safari/537.36',
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36',
                        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36']
        self.page_urls = self.__getAllPageUrls()
        self.page_pointer = -1
        self.savedir = 'resources/succulents'
    '''爬取下一页数据'''
    def next(self):
        # 获取链接
        self.page_pointer += 1
        if self.page_pointer >= len(self.page_urls):
            return True
        page_url = self.page_urls[self.page_pointer]
        # 提取该页中多肉的图片+详情页链接
        res = requests.get(page_url, headers=self.__randomHeaders())
        res.encoding = 'gbk'
        html = etree.HTML(res.text)
        html = html.xpath('//span[@class="tImgUlImg"]')
        succulent_list = []
        for item in html:
            succulent_list.append([item.xpath('a/@title')[0].replace('/', '-').replace('\\', '-'), item.xpath('a/img/@src')[0], item.xpath('a/@href')[0]])
        # 爬取详情页数据
        for item in succulent_list:
            data = [item[0], item[1]]
            headers = self.__randomHeaders()
            headers.update({'Referer': page_url})
            res = requests.get(item[-1], headers=headers)
            res.encoding = 'gbk'
            html_root = etree.HTML(res.text).xpath('//div[@class="cbRight"]/div[@class="mainBox"]')[0]
            html = html_root.xpath('div[2]/table[@class="tTable"]/tr')[1:]
            intro = ['繁殖: ', '易活度: ', '季节: ', '温度: ', '日照: ', '浇水量: ',
                     '日照说明: ', '浇水说明: ', '大类/属: ', '中文种名: ', '英文学名: ']
            for idx, tr in enumerate(html):
                if idx == 0:
                    intro[0] = intro[0] + tr.xpath('./td[2]/text()')[0] if tr.xpath('./td[2]/text()') else intro[0] + '未知'
                    intro[1] = intro[1] + int(tr.xpath('./td[4]/img/@src')[0].split('/')[-1].split('.')[0][1:]) * '⭐'
                elif idx == 1:
                    intro[2] = intro[2] + tr.xpath('./td[2]/text()')[0] if tr.xpath('./td[2]/text()') else intro[2] + '未知'
                    intro[3] = intro[3] + tr.xpath('./td[4]/text()')[0].strip().replace(' ', '') if tr.xpath('./td[4]/text()') else intro[3]
                elif idx == 2:
                    intro[4] = intro[4] + int(tr.xpath('./td[2]/img/@src')[0].split('/')[-1].split('.')[0]) * '☀'
                    intro[5] = intro[5] + int(tr.xpath('./td[4]/img/@src')[0].split('/')[-1].split('.')[0][1:]) * '💧'
            html = html_root.xpath('div[2]/div')[0].xpath('//div[@class="pt5"]')
            for idx, item in enumerate(html):
                if idx == 0:
                    intro[6] = intro[6] + item.xpath('./span/text()')[0]
                elif idx == 1:
                    intro[7] = intro[7] + item.xpath('./span/text()')[0]
                elif idx == 3:
                    intro[8] = intro[8] + item.xpath('text()')[0] if item.xpath('text()') else intro[8] + '未知'
                elif idx == 4:
                    intro[9] = intro[9] + item.xpath('text()')[0] if item.xpath('text()') else intro[9] + '未知'
                elif idx == 5:
                    intro[10] = intro[10] + item.xpath('text()')[0] if item.xpath('text()') else intro[10] + '未知'
            data.append(intro)
            self.__saveItem(data)
            time.sleep(random.random())
        return False
    '''数据保存'''
    def __saveItem(self, data):
        if not os.path.exists(self.savedir):
            os.mkdir(self.savedir)
        savepath = os.path.join(self.savedir, data[0])
        if not os.path.exists(savepath):
            os.mkdir(savepath)
        f = open(os.path.join(savepath, 'show.jpg'), 'wb')
        f.write(requests.get(data[1], headers=self.__randomHeaders()).content)
        f.close()
        f = open(os.path.join(savepath, 'info.pkl'), 'wb')
        pickle.dump(data, f)
        f.close()
    '''获得所有链接'''
    def __getAllPageUrls(self):
        res = requests.get('http://www.mengsang.com/duorou/list_1_1.html', headers=self.__randomHeaders())
        res.encoding = 'gbk'
        html = etree.HTML(res.text)
        num_pages = html.xpath('//span[@class="pageinfo"]/strong')[0].text
        page_urls = ['http://www.mengsang.com/duorou/list_1_%s.html' % i for i in range(1, int(num_pages)+1)]
        return page_urls
    '''随机请求头'''
    def __randomHeaders(self):
        return {'user-agent': random.choice(self.ua_list), 'referer': random.choice(self.referer_list)}