'''
Function:
    特朗普推特生成器
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import js
import sys
import json
import js2py
import random
import requests
import markovify
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


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


'''特朗普推特生成器'''
class TrumpTweetsGenerator(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(TrumpTweetsGenerator, self).__init__(parent)
        # 读取数据, 构建马尔可夫链
        self.tweets = self.readTweets()
        self.markov_model = self.constructMarkov(self.tweets)
        # 定义组件
        self.setWindowTitle('特朗普推特生成器 - 微信公众号:Charles的皮卡丘')
        self.setWindowIcon(QIcon('data/icon.jpg'))
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
    def readTweets(self, filepath='data/trump_tweets.json'):
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
        api = google()
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


'''run'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = TrumpTweetsGenerator()
    client.show()
    sys.exit(app.exec_())