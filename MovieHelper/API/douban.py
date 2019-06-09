'''
Function:
	根据电影名在豆瓣电影里搜索电影信息(脚本仅供学习交流，禁止用于其他)
作者: 
	Charles
微信公众号: 
	Charles的皮卡丘
'''
import re
import sys
import requests
import urllib.parse


'''根据电影名在豆瓣电影里搜索电影信息'''
class Douban():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
						'Host': 'movie.douban.com',
						}
		self.search_url = 'https://movie.douban.com/j/subject_suggest?q={}'
	'''外部调用'''
	def run(self):
		while True:
			# 电影搜索
			movie_name = self.__input('[INFO-豆瓣]请输入需要查询的电影名: ')
			if movie_name == 'restart':
				return False
			res = requests.get(self.search_url.format(urllib.parse.quote(movie_name)), headers=self.headers)
			results = res.json()
			data = dict()
			if len(results) == 0:
				print('[INFO-豆瓣]未能查询到相关关键字的电影信息.')
				continue
			for idx, result in enumerate(results):
				print('——> %d. %s(%s年)' % (idx, result.get('title'), result.get('year')))
				data[str(idx)] = result.get('url')
			# 获得电影详情
			while True:
				movie_idx = self.__input('[INFO-豆瓣]请选择需要了解的电影数字编号: ')
				if movie_idx == 'restart':
					return False
				url = data.get(movie_idx)
				if url is None:
					print('[INFO-豆瓣]您的输入有误, 请重新输入.')
					continue
				else:
					movie_info = requests.get(url, headers=self.headers).text
					directors = self.__refind(r'"director":\[(.*?)\]', movie_info.replace('\n', '').replace(' ', ''))
					if directors != '未知':
						directors = re.findall(r'"name":"(.*?)"', directors)
					directors = '|'.join(directors)
					authors = self.__refind(r'"author":\[(.*?)\]', movie_info.replace('\n', '').replace(' ', ''))
					if authors != '未知':
						authors = re.findall(r'"name":"(.*?)"', authors)
					authors = '|'.join(authors)
					actors = self.__refind(r'"actor":\[(.*?)\]', movie_info.replace('\n', '').replace(' ', ''))
					if actors != '未知':
						actors = re.findall(r'"name":"(.*?)"', actors)
					actors = '|'.join(actors)
					date_published = self.__refind(r'"datePublished": "(.*?)"', movie_info)
					rating = self.__refind(r'"ratingValue": "(.*?)"', movie_info)
					description = self.__refind(r'"description":"(.*?)"', movie_info.replace('\n', '').replace(' ', ''))
					print('[INFO-豆瓣]查询结果如下:\n——> 导演: %s\n——> 编辑: %s\n——> 主演: %s\n——> 上映时间: %s\n——> 豆瓣评分: %s\n——> 简介: %s' % (directors, authors, actors, date_published, rating, description))
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
	'''正则表达式找信息'''
	def __refind(self, rule, text):
		try:
			info = re.findall(rule, text)[0]
		except:
			info = '未知'
		return info