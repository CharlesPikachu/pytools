'''
Function:
	翻译软件V0.1.2,支持:
		--百度翻译
		--有道翻译
		--谷歌翻译
作者:
	Charles
公众号:
	Charles的皮卡丘
'''
import re
import js
import sys
import time
import js2py
import random
import hashlib
import requests
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


'''百度翻译类'''
class baidu():
	def __init__(self):
		self.session = requests.Session()
		self.session.cookies.set('BAIDUID', '19288887A223954909730262637D1DEB:FG=1;')
		self.session.cookies.set('PSTM', '%d;' % int(time.time()))
		self.headers = {
							'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
						}
		self.data = {
						'from': '',
						'to': '',
						'query': '',
						'transtype': 'translang',
						'simple_means_flag': '3',
						'sign': '',
						'token': '',
						'domain': 'common'
					}
		self.url = 'https://fanyi.baidu.com/v2transapi'
		self.langdetect_url = 'https://fanyi.baidu.com/langdetect'
	def translate(self, word):
		self.data['from'] = self.detectLanguage(word)
		self.data['to'] = 'en' if self.data['from'] == 'zh' else 'zh'
		self.data['query'] = word
		self.data['token'], gtk = self.getTokenGtk()
		self.data['token'] = '6482f137ca44f07742b2677f5ffd39e1'
		self.data['sign'] = self.getSign(gtk, word)
		res = self.session.post(self.url, data=self.data)
		return [res.json()['trans_result']['data'][0]['result'][0][1]]
	def getTokenGtk(self):
		url = 'https://fanyi.baidu.com/'
		res = requests.get(url, headers=self.headers)
		token = re.findall(r"token: '(.*?)'", res.text)[0]
		gtk = re.findall(r";window.gtk = ('.*?');", res.text)[0]
		return token, gtk
	def getSign(self, gtk, word):
		evaljs = js2py.EvalJs()
		js_code = js.bd_js_code
		js_code = js_code.replace('null !== i ? i : (i = window[l] || "") || ""', gtk)
		evaljs.execute(js_code)
		sign = evaljs.e(word)
		return sign
	def detectLanguage(self, word):
		data = {
				'query': word
				}
		res = self.session.post(self.langdetect_url, headers=self.headers, data=data)
		return res.json()['lan']


'''有道翻译类'''
class youdao():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
						'Referer': 'http://fanyi.youdao.com/',
						'Cookie': 'OUTFOX_SEARCH_USER_ID=-481680322@10.169.0.83;'
					}
		self.data = {
						'i': None,
						'from': 'AUTO',
						'to': 'AUTO',
						'smartresult': 'dict',
						'client': 'fanyideskweb',
						'salt': None,
						'sign': None,
						'ts': None,
						'bv': None,
						'doctype': 'json',
						'version': '2.1',
						'keyfrom': 'fanyi.web',
						'action': 'FY_BY_REALTlME'
					}
		self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
	def translate(self, word):
		ts = str(int(time.time()*10000))
		salt = ts + str(int(random.random()*10))
		sign = 'fanyideskweb' + word + salt + '97_3(jkMYg@T[KZQmqjTK'
		sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
		bv = '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
		bv = hashlib.md5(bv.encode('utf-8')).hexdigest()
		self.data['i'] = word
		self.data['salt'] = salt
		self.data['sign'] = sign
		self.data['ts'] = ts
		self.data['bv'] = bv
		res = requests.post(self.url, headers=self.headers, data=self.data)
		return [res.json()['translateResult'][0][0].get('tgt')]


'''Google翻译类'''
class google():
	def __init__(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
					}
		self.url = 'https://translate.google.cn/translate_a/single?client=t&sl=auto&tl={}&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&tk={}&q={}'
	def translate(self, word):
		if len(word) > 4891:
			raise RuntimeError('The length of word should be less than 4891...')
		languages = ['zh-CN', 'en']
		if not self.isChinese(word):
			target_language = languages[0]
		else:
			target_language = languages[1]
		res = requests.get(self.url.format(target_language, self.getTk(word), word), headers=self.headers)
		return [res.json()[0][0][0]]
	def getTk(self, word):
		evaljs = js2py.EvalJs()
		js_code = js.gg_js_code
		evaljs.execute(js_code)
		tk = evaljs.TL(word)
		return tk
	def isChinese(self, word):
		for w in word:
			if '\u4e00' <= w <= '\u9fa5':
				return True
		return False


'''简单的Demo'''
class Translator(QWidget):
	def __init__(self, parent=None, **kwargs):
		super(Translator, self).__init__(parent)
		self.setWindowTitle('翻译软件-公众号: Charles的皮卡丘')
		self.setWindowIcon(QIcon('data/icon.jpg'))
		self.Label1 = QLabel('原文')
		self.Label2 = QLabel('译文')
		self.LineEdit1 = QLineEdit()
		self.LineEdit2 = QLineEdit()
		self.translateButton1 = QPushButton()
		self.translateButton2 = QPushButton()
		self.translateButton3 = QPushButton()
		self.translateButton1.setText('百度翻译')
		self.translateButton2.setText('有道翻译')
		self.translateButton3.setText('谷歌翻译')
		self.grid = QGridLayout()
		self.grid.setSpacing(12)
		self.grid.addWidget(self.Label1, 1, 0)
		self.grid.addWidget(self.LineEdit1, 1, 1)
		self.grid.addWidget(self.Label2, 2, 0)
		self.grid.addWidget(self.LineEdit2, 2, 1)
		self.grid.addWidget(self.translateButton1, 1, 2)
		self.grid.addWidget(self.translateButton2, 2, 2)
		self.grid.addWidget(self.translateButton3, 3, 2)
		self.setLayout(self.grid)
		self.resize(400, 150)
		self.translateButton1.clicked.connect(lambda : self.translate(api='baidu'))
		self.translateButton2.clicked.connect(lambda : self.translate(api='youdao'))
		self.translateButton3.clicked.connect(lambda : self.translate(api='google'))
		self.bd_translate = baidu()
		self.yd_translate = youdao()
		self.gg_translate = google()
	def translate(self, api='baidu'):
		word = self.LineEdit1.text()
		if not word:
			return
		if api == 'baidu':
			results = self.bd_translate.translate(word)
		elif api == 'youdao':
			results = self.yd_translate.translate(word)
		elif api == 'google':
			results = self.gg_translate.translate(word)
		else:
			raise RuntimeError('Api should be <baidu> or <youdao> or <google>...')
		self.LineEdit2.setText(';'.join(results))


'''run'''
if __name__ == '__main__':
	app = QApplication(sys.argv)
	demo = Translator()
	demo.show()
	sys.exit(app.exec_())