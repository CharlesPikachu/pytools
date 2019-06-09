'''
Function:
	根据电影名在泡饭影视里搜索电影资源(脚本仅供学习交流，禁止用于其他)
作者: 
	Charles
微信公众号: 
	Charles的皮卡丘
'''
import re
import sys
import requests
from bs4 import BeautifulSoup


'''泡饭影视'''
class Paofan():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
					}
		self.search_url = 'http://www.chapaofan.com/search/{}'
	'''外部调用'''
	def run(self):
		while True:
			# 关键字搜索
			movie_name = self.__input('[INFO-泡饭]请输入需要搜索的电影名: ')
			if movie_name == 'restart':
				return False
			res = requests.get(self.search_url.format(movie_name), headers=self.headers)
			soup = BeautifulSoup(res.text, 'lxml')
			movies_list = soup.find_all('div', attrs={'class': 'content-side-left'})
			if len(movies_list) == 0:
				print('[INFO-泡饭]未能查询到相关关键字的电影信息.')
				continue
			movies_list = movies_list[0].find_all('ul', attrs={'class': 'item'})
			data = dict()
			if len(movies_list) == 0:
				print('[INFO-泡饭]未能查询到相关关键字的电影信息.')
				continue
			for idx, each in enumerate(movies_list):
				name = each.li.string.strip()
				url = each.li.a.get('href')
				print('——> %d. %s' % (idx, name))
				data[str(idx)] = url + '#download-area'
			# 获得电影资源
			while True:
				movie_idx = self.__input('[INFO-泡饭]请选择想要的电影资源编号: ')
				if movie_idx == 'restart':
					return False
				url = data.get(movie_idx)
				if url is None:
					print('[INFO-泡饭]您的输入有误, 请重新输入.')
					continue
				else:
					res = requests.get(url, headers=self.headers)
					links = re.findall(r'"(ed2k.*?)"', res.text) + re.findall(r'"(thunder.*?)"', res.text) + re.findall(r'"(magnet.*?)"', res.text)
					if len(links) == 0:
						print('[INFO-泡饭]抱歉, 未找到该电影的资源链接.')
					else:
						filname = 'paofan_search_%s.links' % movie_name
						print('[INFO-泡饭]电影资源链接有(已保存在%s):' % filname)
						f = open(filname, 'w')
						for link in links:
							print('——> %s' % link)
							f.write(link + '\n')
						f.close()
					break
		return True
	'''处理用户输入'''
	def __input(self, info):
		user_input = input(info)
		if user_input == 'q' or user_input == 'Q':
			sys.exit(0)
		elif user_input == 'r' or user_input == 'R':
			return 'restart'
		else:
			return user_input