'''
Function:
    特朗普推特生成器
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import json
import time
import random
import hashlib
import requests
import markovify
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


'''有道翻译'''
class YoudaoTranslator():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Referer': 'http://fanyi.youdao.com/',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-481680322@10.169.0.83;'
        }
        self.data = {
            'i': None, 'from': 'AUTO', 'to': 'AUTO', 'smartresult': 'dict',
            'client': 'fanyideskweb', 'salt': None, 'sign': None, 'lts': None,
            'bv': None, 'doctype': 'json', 'version': '2.1', 'keyfrom': 'fanyi.web', 'action': 'FY_BY_REALTlME'
        }
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    '''翻译'''
    def translate(self, word):
        lts = str(int(time.time() * 10000))
        salt = lts + str(int(random.random() * 10))
        sign = 'fanyideskweb' + word + salt + 'Y2FYu%TNSbMCxc3t2u^XT'
        sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
        bv = '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        bv = hashlib.md5(bv.encode('utf-8')).hexdigest()
        self.data['i'] = word
        self.data['salt'] = salt
        self.data['sign'] = sign
        self.data['lts'] = lts
        self.data['bv'] = bv
        response = requests.post(self.url, headers=self.headers, data=self.data)
        return [response.json()['translateResult'][0][0].get('tgt')]


'''特朗普推特生成器'''
class TrumpTweetsGenerator(QWidget):
    tool_name = '特朗普推特生成器'
    def __init__(self, parent=None, title='特朗普推特生成器 —— Charles的皮卡丘', **kwargs):
        super(TrumpTweetsGenerator, self).__init__(parent)
        rootdir = os.path.split(os.path.abspath(__file__))[0]
        # 读取数据, 构建马尔可夫链
        self.tweets = self.readTweets(os.path.join(rootdir, 'resources/trump_tweets.json'))
        self.markov_model = self.constructMarkov(self.tweets)
        # 定义组件
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(os.path.join(rootdir, 'resources/icon.jpg')))
        self.setFixedSize(600, 400)
        self.label_result = QLabel('生成的结果:')
        self.button_generate = QPushButton('生成特朗普推特')
        self.button_translate = QPushButton('翻译特朗普推特')
        self.text_result = QTextEdit()
        # 布局
        self.grid = QGridLayout()
        self.grid.addWidget(self.label_result, 0, 0, 1, 1)
        self.grid.addWidget(self.button_generate, 0, 8, 1, 1)
        self.grid.addWidget(self.button_translate, 0, 9, 1, 1)
        self.grid.addWidget(self.text_result, 1, 0, 1, 10)
        self.setLayout(self.grid)
        # 事件绑定
        self.button_generate.clicked.connect(self.generateTweet)
        self.button_translate.clicked.connect(self.translate)
    '''推特数据读取'''
    def readTweets(self, filepath=None):
        fp = open(filepath, 'r', encoding='utf-8')
        tweets = json.load(fp)
        all_infos = {'hashtags': [], 'mentions': [], 'contents': []}
        for tweet in tweets:
            words = tweet['text'].split(' ')
            for word in words:
                if not word: continue
                if word[0] == '#':
                    all_infos['hashtags'].append(word)
                if word[0] == '@' and len(word) > 1:
                    all_infos['mentions'].append(word)
            all_infos['contents'].append(tweet['text'])
        return all_infos
    '''构建马尔可夫链'''
    def constructMarkov(self, tweets):
        text = ''.join(tweets['contents'])
        markov_model = markovify.Text(text)
        return markov_model
    '''生成推特'''
    def generateTweet(self):
        tweet = self.markov_model.make_sentence()
        if random.random() > 0.7:
            tweet = random.choice(self.tweets['mentions']) + tweet
        if random.random() > 0.9:
            tweet = tweet + random.choice(self.tweets['hashtags'])
        self.text_result.setText(tweet)
        return tweet
    '''翻译当前的推特'''
    def translate(self):
        api = YoudaoTranslator()
        tweet = self.text_result.toPlainText()
        translated_tweet = '翻译接口调用失败'
        if tweet:
            try:
                translated_tweet = ' '.join(api.translate(tweet))
            except:
                pass
        text = '原文: %s\n\n译文: %s' % (tweet, translated_tweet)
        self.text_result.setText(text)
        return translated_tweet