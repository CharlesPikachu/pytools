# 作者: Charles
# 公众号: Charles的皮卡丘
# 根据电影名在豆瓣电影里搜索电影信息
# 脚本仅供学习交流，禁止用于其他
import re
import json
import requests


# 根据电影名在豆瓣电影里搜索电影信息
class douban():
	def __init__(self):
		self.headers = {
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
						'Accept-Encoding': 'gzip, deflate, br',
						'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
						'Connection': 'keep-alive',
						'Host': 'movie.douban.com',
						'Referer': 'https://movie.douban.com/',
						'Upgrade-Insecure-Requests': '1',
						'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
						}
		self.search_url = 'https://movie.douban.com/subject_search?search_text={}&cat=1002'
		self.suggest_url = 'https://movie.douban.com/j/subject_suggest?q={}'
	# 外部调用
	def search(self, keyword):
		movies_info = self.__get_search_result(keyword)
		options = self.__print_search_result(movies_info)
		while True:
			choice = input('请输入需要了解的电影编号: ')
			url = options.get(choice)
			if url:
				print('您选择了第%s部电影, 现在开始检索该电影信息' % choice)
				break
			else:
				print('您的输入有误，请重新输入。')
		movie_info = self.__get_movie_info(url[0])
		self.__print_movie_info(movie_info)
		return movie_info
	# 获得按照给定关键词搜索后的搜索结果信息
	def __get_search_result(self, keyword):
		movies_info = {}
		res = requests.get(self.suggest_url.format(keyword), headers=self.headers)
		res_json = json.loads(res.text)
		for movie in res_json:
			movies_info[movie['title']] = [movie['url'], movie['type'], movie['year'], movie['sub_title'], movie['id']]
		return movies_info
	# 获得某个具体电影的详细信息
	def __get_movie_info(self, url):
		movie_info = {}
		res = requests.get(url, headers=self.headers)
		director = self.__refind(r'"v:directedBy"\>(.+?)\<', res.text, idx=0)
		temp = self.__refind(r'"v:starring"\>(.+?)\<', res.text, idx='all')
		starrings = '|'.join(temp)
		temp = self.__refind(r'"v:genre"\>(.+?)\<', res.text, idx='all')
		genres = '|'.join(temp)
		temp = self.__refind(r'"v:initialReleaseDate".*?>(.+?)\<', res.text, idx='all')
		ReleaseDates = '|'.join(temp)
		runtime = self.__refind(r'"v:runtime".*?>(.+?)\<', res.text, idx=0)
		score = self.__refind(r'"v:average"\>(.+?)\<', res.text, idx=0)
		movie_info['director'] = director
		movie_info['starrings'] = starrings
		movie_info['genres'] = genres
		movie_info['ReleaseDates'] = ReleaseDates
		movie_info['runtime'] = runtime
		movie_info['score'] = score
		return movie_info
	# 打印搜索结果信息
	def __print_search_result(self, movies_info):
		options = {}
		i = 0
		print('=' * 60)
		if movies_info:
			print('共搜索到%d部相关电影, 结果如下:' % len(movies_info.keys()))
			for key, value in movies_info.items():
				i += 1
				name = key if key == value[3] else key + '(%s)' % value[3]
				print('[%d].<Movie Name>: %s, <Year>: %s' % (i, name, value[2]))
				options[str(i)] = [value[0], key]
		else:
			print('抱歉，没有找到相关电影。')
		print('=' * 60)
		return options
	# 打印电影信息
	def __print_movie_info(self, movie_info):
		print('=' * 60)
		if movie_info:
			print('该电影的详细信息如下:')
			print('[导演]: %s' % movie_info.get('director'))
			print('[主演]: %s' % movie_info.get('starrings'))
			print('[类型]: %s' % movie_info.get('genres'))
			print('[上映日期]: %s' % movie_info.get('ReleaseDates'))
			print('[片长]: %s' % movie_info.get('runtime'))
			print('[豆瓣评分]: %s' % movie_info.get('score'))
		else:
			print('抱歉，没有找到该电影的信息。')
		print('=' * 60)
	# 通过正则表达式找数据
	def __refind(self, rule, content, idx=0):
		try:
			if idx == 'all':
				result = re.findall(rule, content)
			else:
				result = re.findall(rule, content)[idx]
		except:
			result = '未知'
		return result