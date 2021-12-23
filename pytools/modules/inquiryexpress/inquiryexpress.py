'''
Function:
    快递查询系统
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import time
import pickle
import random
import requests
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui


'''快递查询系统'''
class InquiryExpress(QWidget):
    tool_name = '快递查询系统'
    def __init__(self, parent=None, title='快递查询系统 —— Charles的皮卡丘', **kwargs):
        super(InquiryExpress, self).__init__(parent)
        rootdir = os.path.split(os.path.abspath(__file__))[0]
        self.companies = pickle.load(open(os.path.join(rootdir, 'resources/companies.pkl'), 'rb'))
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(os.path.join(rootdir, 'resources/icon.jpg')))
        self.label1 = QLabel('快递单号:')
        self.line_edit = QLineEdit()
        self.label2 = QLabel('查询结果:')
        self.text = QTextEdit()
        self.button = QPushButton()
        self.button.setText('查询')
        self.grid = QGridLayout()
        self.grid.addWidget(self.label1, 1, 0)
        self.grid.addWidget(self.line_edit, 1, 1, 1, 39)
        self.grid.addWidget(self.button, 1, 40)
        self.grid.addWidget(self.label2, 2, 0)
        self.grid.addWidget(self.text, 2, 1, 1, 40)
        self.setLayout(self.grid)
        self.setFixedSize(600, 400)
        self.button.clicked.connect(self.inquiry)
    '''查询'''
    def inquiry(self):
        number = self.line_edit.text()
        try:
            infos = self.getExpressInfo(number)
            if not infos: infos = ['-' * 40 + '\n' + '单号不存在或已过期\n' + '-' * 40 + '\n']
        except:
            infos = ['-' * 40 + '\n' + '快递单号有误, 请重新输入.\n' + '-' * 40 + '\n']
        self.text.setText('\n\n\n'.join(infos)[:-1])
    '''利用快递100查询快递'''
    def getExpressInfo(self, number):
        session = requests.Session()
        # 获得快递公司信息
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Host': 'm.kuaidi100.com'
        }
        infos = []
        express_info = session.get(f'http://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text={number}', headers=headers).json()['auto'][0]
        # 查询快递
        url = 'https://m.kuaidi100.com/query'
        data = {
            'postid': number,
            'id': '1',
            'valicode': '',
            'temp': str(random.random()),
            'type': express_info['comCode'],
            'phone': '',
            'token': '',
            'platform': 'MWWW',
        }
        headers['Cookie'] = f'csrftoken=Rho5YwzYpY8Mhove9XuhD83akWBd2QV3S-bpBcc3OhA; _adadqeqwe1321312dasddocTitle=kuaidi100; _adadqeqwe1321312dasddocReferrer=; _adadqeqwe1321312dasddocHref=; WWWID=WWW325CDE0C596CC0AA6F456439F7220990; Hm_lvt_22ea01af58ba2be0fec7c11b25e88e6c=1640252974,1640252990,1640253001; Hm_lpvt_22ea01af58ba2be0fec7c11b25e88e6c={int(time.time())}'
        response_json = session.post(url, headers=headers, data=data).json()
        express_data, infos = response_json['data'], []
        if ('name' in express_info) and express_info['name']:
            info = '公司: %s\n' % express_info['name']
        else:
            info = '公司: %s\n' % self.py2hz(company_name)
        for idx, item in enumerate(express_data):
            if idx == 0:
                info += '-' * 40 + '\n时间:\n' + item['time'] + '\n进度:\n' + item['context'] + '\n' + '-' * 40 + '\n'
            else:
                info += '时间:\n' + item['time'] + '\n进度:\n' + item['context'] + '\n' + '-' * 40 + '\n'
        if not express_data:
            info += '-' * 40 + '\n' + '单号不存在或已过期\n' + '-' * 40 + '\n'
        infos.append(info)
        return infos
    '''将快递公司的拼音变为汉字'''
    def py2hz(self, py):
        return self.companies.get(py)