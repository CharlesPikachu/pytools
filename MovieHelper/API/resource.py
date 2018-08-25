# 作者: Charles
# 公众号: Charles的皮卡丘
# 根据电影名搜索电影资源的下载链接
# 脚本仅供学习交流，禁止用于其他
# 目前支持的搜索平台: 
# 	泡饭影视: http://www.chapaofan.com/
# 	BT电影天堂: https://www.bttt.la/
import re
import requests
from bs4 import BeautifulSoup
TIPS = u'以上链接为互联网抓取，所有资源版权归原权利人，如有网友通过本脚本下载资源，请下载后24小时内删除，勿将下载的免费资源用于商业用途。'


'''
Function:
	在BT电影天堂搜索电影资源
'''
class bt():
	def __init__(self):
		self.headers = {
						'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
						}
		self.host = 'https://www.bttt.la'
		self.search_url = 'https://www.bttt.la/s.php?q={}&sitesearch=www.bttt.la&domains=bttt.la&hl=zh-CN&ie=UTF-8&oe=UTF-8'
		self.info_url = 'https://www.bttt.la/subject/{}.html'
	# 外部调用
	def search(self, keyword):
		results = self.__get_search_results(keyword)
		self.__print_search_results(results)
		while True:
			choice = input('请输入想要下载的电影编号: ')
			movie_name = results.get(choice)
			if movie_name:
				print('你选择了电影《%s》, 编号%s, 现在开始获取资源链接。' % (movie_name, choice))
				break
			else:
				print('您的输入有误，请重新输入。')
		links = self.__get_movie_link(choice)
		self.__print_movie_links(links)
		return links
	# 根据关键词搜索
	def __get_search_results(self, keyword):
		res = requests.get(self.search_url.format(keyword), headers=self.headers)
		soup = BeautifulSoup(res.text, 'lxml')
		temp1 = soup.find_all('div', attrs={'class': 'ml'})
		temp2 = re.findall(r'"/subject/(\d+?)\.html".*?\<b\>(.*?)\</b\>', str(temp1))
		results = {}
		for t in temp2:
			if t[1]:
				soup = BeautifulSoup(t[1], 'lxml')
				results[t[0]] = soup.text
		return results
	# 根据电影编号获取电影资源链接
	def __get_movie_link(self, movie_id):
		res = requests.get(self.info_url.format(movie_id), headers=self.headers)
		soup = BeautifulSoup(res.content, 'lxml')
		temp = soup.find_all('div', attrs={'class': 'tinfo'})
		links = {}
		for t in temp:
			url = self.host + t.find_all('a', attrs={'href': True})[0]['href']
			res = requests.get(url, headers=self.headers)
			soup = BeautifulSoup(res.text, 'lxml')
			link = soup.find_all('div', attrs={'style': 'position:relative'})[1].text
			title = t.find_all('a', attrs={'href': True})[0]['title']
			links[title] = link
		return links
	# 打印搜索结果
	def __print_search_results(self, results):
		print('=' * 60)
		if results:
			print('搜索到%d个相关资源:' % len(results.keys()))
			for key, value in results.items():
				print('[电影编号]: %s,[电影名]: %s' % (key, value))
		else:
			print('抱歉，没有找到相关资源。')
		print('=' * 60)
	# 打印获取电影资源链接结果
	def __print_movie_links(self, links):
		print('=' * 60)
		if links:
			print('资源获取成功, 电影资源下载链接为:')
			for key, value in links.items():
				print("%s:\n%s" % (str(key), str(value)))
			print(TIPS)
		else:
			print('抱歉，电影资源链接获取失败。')
		print('=' * 60)


'''
Function:
	在泡饭影视搜索电影资源
'''
class paofan():
	def __init__(self):
		self.headers = {
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
						'Accept-Encoding': 'gzip, deflate',
						'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
						'Connection': 'keep-alive',
						'Host': 'www.chapaofan.com',
						'Referer': 'http://www.chapaofan.com/search',
						'Upgrade-Insecure-Requests': '1',
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
					}
		self.search_url = "http://www.chapaofan.com/search/{}"
		self.info_url = "http://www.chapaofan.com/{}.html"
	# 外部调用
	def search(self, keyword):
		results = self.__get_search_results(keyword)
		self.__print_search_results(results)
		while True:
			choice = input('请输入想要下载的电影编号: ')
			movie_name = results.get(choice)
			if movie_name:
				print('你选择了电影《%s》, 编号%s, 现在开始获取资源链接。' % (movie_name, choice))
				break
			else:
				print('您的输入有误，请重新输入。')
		links = self.__get_movie_link(choice)
		self.__print_movie_links(links)
		return links
	# 根据关键词搜索
	def __get_search_results(self, keyword):
		res = requests.get(self.search_url.format(keyword), headers=self.headers)
		soup = BeautifulSoup(res.text, 'lxml')
		temp1 = soup.find_all('div', attrs={'class': 'content-list'})
		temp2 = re.findall(r'http://www\.chapaofan\.com/(\d+?)\.html.*?\>(.*?)\<', str(temp1))
		results = {}
		for t in temp2:
			if t[1]:
				results[t[0]] = t[1]
		return results
	# 根据电影编号获取电影资源链接
	def __get_movie_link(self, movie_id):
		res = requests.get(self.info_url.format(movie_id), headers=self.headers)
		soup = BeautifulSoup(res.text, 'lxml')
		temp = soup.select(".download-list > ul > li > a")
		links = {}
		for t in temp:
			links[t.text.replace(' ', '').replace('\n', '')] = t['href']
		return links
	# 打印搜索结果
	def __print_search_results(self, results):
		print('=' * 60)
		if results:
			print('搜索到%d个相关资源:' % len(results.keys()))
			for key, value in results.items():
				print('[电影编号]: %s,[电影名]: %s' % (key, value))
		else:
			print('抱歉，没有找到相关资源。')
		print('=' * 60)
	# 打印获取电影资源链接结果
	def __print_movie_links(self, links):
		print('=' * 60)
		if links:
			print('资源获取成功, 电影资源下载链接为:')
			for key, value in links.items():
				print("%s:\n%s" % (str(key), str(value)))
			print(TIPS)
		else:
			print('抱歉，电影资源链接获取失败。')
		print('=' * 60)