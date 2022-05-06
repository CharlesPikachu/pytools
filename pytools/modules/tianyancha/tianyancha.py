'''
Function:
    天眼查
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import requests
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui


'''天眼查'''
class Tianyancha(QWidget):
    tool_name = '天眼查'
    def __init__(self, parent=None, title='天眼查 —— Charles的皮卡丘', **kwargs):
        super(Tianyancha, self).__init__(parent)
        rootdir = os.path.split(os.path.abspath(__file__))[0]
        self.setFixedSize(800, 500)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(os.path.join(rootdir, 'resources/icon.jpeg')))
        # 定义一些必要的组件
        grid = QGridLayout()
        # --标签
        label = QLabel('想要查询的公司名:')
        # --输入框
        self.edit = QLineEdit()
        self.edit.setText('万门大学')
        # --生成按钮
        button_query = QPushButton('查询公司')
        # --结果显示框
        self.text_edit = QTextEdit()
        # 组件布局
        grid.addWidget(label, 0, 0, 1, 1)
        grid.addWidget(self.edit, 0, 1, 1, 1)
        grid.addWidget(button_query, 1, 0, 1, 2)
        grid.addWidget(self.text_edit, 2, 0, 5, 2)
        self.setLayout(grid)
        # 事件绑定
        button_query.clicked.connect(self.query)
    '''查询公司'''
    def query(self):
        company_name = self.edit.text()
        # 获取基本信息
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'version': 'TYC-XCX-WX',
            'Host': 'api9.tianyancha.com',
            'Authorization': '0###oo34J0VKzLlpdvf8kgFkMlfU_IPY###1642087379312###22494f3155c2e5a4be76e503837fa439',
            'x-auth-token': 'eyJkaXN0aW5jdF9pZCI6IjE3ZDFjNWVhMzZjNGY2LTA5ZjU2NWUwNWViNTZjLTFjMzA2ODUxLTIwNzM2MDAtMTdkMWM1ZWEzNmRiMzYiLCJsaWIiOnsiJGxpYiI6ImpzIiwiJGxpYl9tZXRob2QiOiJjb2RlIiwiJGxpYl92ZXJzaW9uIjoiMS4xNS4yNCJ9LCJwcm9wZXJ0aWVzIjp7IiR0aW1lem9uZV9vZmZzZXQiOi00ODAsIiRzY3JlZW5faGVpZ2h0IjoxMDgwLCIkc2NyZWVuX3dpZHRoIjoxOTIwLCIkbGliIjoianMiLCIkbGliX3ZlcnNpb24iOiIxLjE1LjI0IiwiJGxhdGVzdF90cmFmZmljX3NvdXJjZV90eXBlIjoi6Ieq54S25pCc57Si5rWB6YePIiwiJGxhdGVzdF9zZWFyY2hfa2V5d29yZCI6IuacquWPluWIsOWAvCIsIiRsYXRlc3RfcmVmZXJyZXIiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyIsImN1cnJlbnRfdXJsIjoiaHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vc2VhcmNoP2tleT0lRTYlOUQlQUQlRTUlQjclOUUlRTYlOTklQUUlRTUlODUlQjQlRTQlQkMlODElRTQlQjglOUElRTclQUUlQTElRTclOTAlODYlRTUlOTAlODglRTQlQkMlOTklRTQlQkMlODElRTQlQjglOUEiLCJyZWZlcnJlciI6Imh0dHBzOi8vd3d3LnRpYW55YW5jaGEuY29tL3NlYXJjaD9rZXk9JUU2JTlEJUFEJUU1JUI3JTlFJUU2JTk5JUFFJUU1JTg1JUI0JUU0JUJDJTgxJUU0JUI4JTlBJUU3JUFFJUExJUU3JTkwJTg2JUU1JTkwJTg4JUU0JUJDJTk5JUU0JUJDJTgxJUU0JUI4JTlBIiwidHljaWQiOiI0MmMxZTY1MDQ0ZjYxMWVjYmIxZDY3ZmJiYzEwN2U3NSIsIm5hbWUiOiLmna3lt57mma7lhbTkvIHkuJrnrqHnkIblkIjkvJnkvIHkuJoiLCJtb2R1bGUiOiLkvJjotKjlrp7lkI3orqTor4EiLCIkaXNfZmlyc3RfZGF5IjpmYWxzZX0sImFub255bW91c19pZCI6IjE3ZDFjNWVhMzZjNGY2LTA5ZjU2NWUwNWViNTZjLTFjMzA2ODUxLTIwNzM2MDAtMTdkMWM1ZWEzNmRiMzYiLCJ0eXBlIjoidHJhY2siLCJldmVudCI6InNlYXJjaF9yZXN1bHRfZXhwdXJlIiwiX3RyYWNrX2lkIjo3MjUyNDM3Mjd9',
        }
        url = f'https://api9.tianyancha.com/services/v3/search/sNorV3/{company_name}'
        response = requests.get(url, headers=headers)
        response_json, data = response.json(), dict()
        if response_json['state'] == 'ok':
            data = response_json.get('data', {})
        # 基本信息提取
        company_info = {'未查询到该公司相关的信息': ''}
        if data:
            company, brand_and_agency = data['companyList'][0], {}
            for item in data['brandAndAgencyList']:
                if item['graphId'] == company['id']:
                    brand_and_agency = item
                    break
            detail = requests.get(f'https://api9.tianyancha.com/services/v3/t/common/baseinfoV5/{company["id"]}', headers=headers).json().get('data', {})
            company_info = {
                '公司外部系统ID': company.get('id', ''),
                '公司名称': company.get('name', '').replace('<em>', '').replace('</em>', ''),
                '公司简称 ': company.get('alias', ''),
                '公司法人': company.get('legalPersonName', ''),
                '公司成立时间': company.get('estiblishTime', '')[:10],
                '公司注册地址': company.get('regLocation', ''),
                '公司所在省份': company.get('base', ''),
                '公司所在市': company.get('city', ''),
                '公司所在区': company.get('district', ''),
                '公司经营状态': company.get('regStatus', ''),
                '公司地址经纬度坐标': (company.get('latitude', ''), company.get('longitude', '')),
                '公司邮箱列表': company.get('emails', '').split(';')[0].replace('\t', ''),
                '公司联系方式列表': company.get('phoneList', ''),
                '公司联系方式': company.get('phoneNum', ''),
                '公司经营范围': company.get('businessScope', ''),
                '公司类型': company.get('companyOrgType', '').replace('\t', ''),
                '公司质量分数': company.get('orginalScore', ''),
                '公司注册资本': company.get('regCapital', ''),
                '公司统一社会信用代码': company.get('creditCode', ''),
                '公司纳税号': company.get('taxCode', '') or company.get('creditCode', ''),
                '公司注册号': company.get('regNumber', ''),
                '公司组织机构代码': company.get('orgNumber', ''),
                '公司标签列表': company.get('labelListV2', ''),
                '公司行业分类': company.get('categoryStr', ''),
                '公司融资轮次': brand_and_agency.get('round', ''),
                '公司竟品信息': brand_and_agency.get('jingpinName', ''),
                '公司logo': brand_and_agency.get('logo', '') or detail.get('logo', ''),
                '公司简介': brand_and_agency.get('intro', '') or detail.get('baseInfo', ''),
                '公司英文名': detail.get('property3', '') or detail.get('nameEn', ''),
                '公司注册机构': detail.get('regInstitute', ''),
                '公司网站地址集': detail.get('websiteList', ''),
                '公司实缴资本': detail.get('actualCapital', ''),
                '公司曾用名': detail.get('historyNames', ''),
                '公司员工人数': detail.get('socialStaffNum', '') or detail.get('staffNum', ''),
                '公司纳税地址': detail.get('taxAddress', '') or detail.get('regLocation', ''),
                '公司纳税银行': detail.get('taxBankName', ''), 
                '公司涉足领域标签': detail.get('portray', ''), 
            }
        # 打印
        company_info_str = ''
        for key, value in company_info.items():
            company_info_str += f'{key}: {value}\n'
        self.text_edit.setText(company_info_str)