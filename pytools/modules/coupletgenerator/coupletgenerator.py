'''
Function:
    对联生成器
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import json
import random
import requests
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui


'''对联生成器'''
class CoupletGenerator(QWidget):
    tool_name = '对联生成器'
    def __init__(self, parent=None, title='对联生成器 —— Charles的皮卡丘', api_key='gO8GyW0haswcHXVisDOngByI', secret_key='QQzxxlV58VjWfWFELjKGVBU7oktrhSNR', **kwargs):
        super(CoupletGenerator, self).__init__(parent)
        assert api_key and secret_key, '请到https://console.bce.baidu.com/#/index/overview申请对联生成器所需的api_key和secret_key'
        rootdir = os.path.split(os.path.abspath(__file__))[0]
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(os.path.join(rootdir, 'resources/icon.png')))
        self.setFixedSize(600, 400)
        self.error_codes = {
            '2': '后端连接超时请重试',
            '52001': '请求超时请重试',
            '52002': '系统错误请重试',
            '52003': '未授权用户',
            '52004': '输入解析失败',
            '52005': '输入字段有误',
            '52006': '输入文本长度不超过5',
            '52007': '输入文本包含政治&黄色内容',
            '52008': '后台服务返回错误请重试',
            '54003': '访问频率受限',
            '54100': '查询接口参数为空',
            '54102': '无写诗结果请重试'
        }
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = self.gettoken()
        # 设置组件
        self.label_title = QLabel('春联主题:')
        self.line_title = QLineEdit('新春佳节')
        self.generate_btn = QPushButton('生成')
        self.label_result = QLabel('生成结果:')
        self.text_couple = QTextEdit()
        # 布局
        grid = QGridLayout()
        grid.addWidget(self.label_title, 1, 0)
        grid.addWidget(self.line_title, 1, 1, 1, 39)
        grid.addWidget(self.generate_btn, 1, 40)
        grid.addWidget(self.label_result, 2, 0)
        grid.addWidget(self.text_couple, 2, 1, 1, 40)
        self.setLayout(grid)
        # 事件关联
        self.generate_btn.clicked.connect(self.generate)
    '''生成对联'''
    def generate(self):
        if not self.line_title.text().strip():
            return
        url = f'https://aip.baidubce.com/rpc/2.0/nlp/v1/couplets?access_token={self.access_token}'
        headers = {
            'Content-Type': 'application/json'
        }
        all_couplets = []
        index_ranges = [(0, 2), (3, 5), (6, 8), (9, 11), (12, 14)]
        for idx in range(5):
            params = {
                'text': self.line_title.text(),
                'index': random.randint(*index_ranges[idx]),
            }
            response = requests.post(url, headers=headers, json=params)
            response_json = response.json()
            center = response_json['couplets']['center']
            first = response_json['couplets']['first']
            second = response_json['couplets']['second']
            text = f'横批: {center}\n上联: {first}\n下联: {second}'
            all_couplets.append(text)
        self.text_couple.setText('\n\n\n'.join(all_couplets))
    '''获取token'''
    def gettoken(self):
        url = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.api_key}&client_secret={self.secret_key}'
        headers = {
            'Content-Type': 'application/json; charset=UTF-8'
        }
        response = requests.get(url, headers=headers)
        access_token = response.json()['access_token']
        return access_token