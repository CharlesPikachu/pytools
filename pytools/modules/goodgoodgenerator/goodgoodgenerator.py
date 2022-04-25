'''
Function:
    稳中向好生成器
Author:
    Charles
微信公众号:
    Charle的皮卡丘
'''
import os
import json
import random
import pyttsx3
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui


'''稳中向好生成器'''
class GoodGoodGenerator(QWidget):
    tool_name = '稳中向好生成器'
    def __init__(self, parent=None, title='稳中向好生成器 —— Charles的皮卡丘', **kwargs):
        super(GoodGoodGenerator, self).__init__(parent)
        rootdir = os.path.split(os.path.abspath(__file__))[0]
        self.setFixedSize(800, 500)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(os.path.join(rootdir, 'resources/icon.jpg')))
        self.resources = json.load(open(os.path.join(rootdir, 'resources/data.json'), 'r', encoding='utf-8'))
        self.article = None
        # 定义一些必要的组件
        grid = QGridLayout()
        # --标签
        label_1 = QLabel('稳中向好的事件主题:')
        label_2 = QLabel('生成的文章字数:')
        # --输入框
        self.edit_1 = QLineEdit()
        self.edit_1.setText('年轻人买房')
        self.edit_2 = QLineEdit()
        self.edit_2.setText('500')
        # --生成按钮
        button_generate = QPushButton('生成稳中向好文章')
        # --朗读按钮
        button_deacon = QPushButton('朗读生成的文章')
        # --结果显示框
        self.text_edit = QTextEdit()
        # 组件布局
        grid.addWidget(label_1, 0, 0, 1, 1)
        grid.addWidget(self.edit_1, 0, 1, 1, 1)
        grid.addWidget(label_2, 1, 0, 1, 1)
        grid.addWidget(self.edit_2, 1, 1, 1, 1)
        grid.addWidget(button_generate, 2, 0, 1, 2)
        grid.addWidget(button_deacon, 3, 0, 1, 2)
        grid.addWidget(self.text_edit, 4, 0, 5, 2)
        self.setLayout(grid)
        # 事件绑定
        button_generate.clicked.connect(self.generate)
        button_deacon.clicked.connect(self.deacon)
    '''朗诵稳中向好文章'''
    def deacon(self):
        pyttsx3.speak(self.article)
    '''生成稳中向好文章'''
    def generate(self):
        # 分配开头, 结尾和主体内容的字数
        num_words = int(self.edit_2.text())
        begin_num_words, body_num_words, end_num_words = num_words * 0.15, num_words * 0.7, num_words * 0.15
        # 主题
        theme = self.edit_1.text()
        # 生成标题
        title = self.generatetitle(theme)
        # 生成文章开头
        begin = self.generatebegin(begin_num_words, theme)
        # 生成文章主体
        body = self.generatebody(body_num_words, theme)
        # 生成文章结尾
        end = self.generateend(end_num_words, theme)
        # 整合文章
        self.article = f'{title}\n    {begin}\n    {body}\n    {end}'
        # 显示文章
        self.text_edit.setText(self.article)
    '''替换原始内容中的占位符'''
    def replace(self, input_str, theme):
        # vn
        while input_str.find('vn') != -1:
            total = len(self.resources['verb']) - 1
            verb = self.resources['verb'][random.randint(0, total)]
            total = len(self.resources['noun']) - 1
            noun = self.resources['noun'][random.randint(0, total)]
            vn = '，'.join([verb + noun for i in range(random.randint(1, 4))])
            input_str = input_str.replace('vn', vn, 1)
        # v
        while input_str.find('v') != -1:
            total = len(self.resources['verb']) - 1
            verb = self.resources['verb'][random.randint(0, total)]
            input_str = input_str.replace('v', verb, 1)
        # n
        while input_str.find('n') != -1:
            total = len(self.resources['noun']) - 1
            noun = self.resources['noun'][random.randint(0, total)]
            input_str = input_str.replace('n', noun, 1)
        # ss
        while input_str.find('ss') != -1:
            total = len(self.resources['sentence']) - 1
            sentence = self.resources['sentence'][random.randint(0, total)]
            input_str = input_str.replace('ss', sentence, 1)
        # sp
        while input_str.find('sp') != -1:
            total = len(self.resources['parallel_sentence']) - 1
            parallel_sentence = self.resources['parallel_sentence'][random.randint(0, total)]
            input_str = input_str.replace('sp', parallel_sentence, 1)
        # p
        while input_str.find('p') != -1:
            total = len(self.resources['phrase']) - 1
            phrase = self.resources['phrase'][random.randint(0, total)]
            input_str = input_str.replace('p', phrase, 1)
        # xx
        input_str = input_str.replace('xx', theme)
        # return
        return input_str
    '''生成文章标题'''
    def generatetitle(self, theme):
        total = len(self.resources['title']) - 1
        title = self.resources['title'][random.randint(0, total)]
        return self.replace(title, theme)
    '''生成文章开头'''
    def generatebegin(self, begin_num_words, theme):
        begin = ''
        while len(begin) < begin_num_words: 
            total = len(self.resources['beginning']) - 1
            begin += self.replace(self.resources['beginning'][random.randint(0, total)], theme)
        return begin
    '''生成文章结尾'''
    def generateend(self, end_num_words, theme):
        end = ''
        while len(end) < end_num_words: 
            total = len(self.resources['ending']) - 1
            end += self.replace(self.resources['ending'][random.randint(0, total)], theme)
        return end
    '''生成文章主体'''
    def generatebody(self, body_num_words, theme):
        body = ''
        while len(body) < body_num_words: 
            total = len(self.resources['body']) - 1
            body += self.replace(self.resources['body'][random.randint(0, total)], theme)
        return body