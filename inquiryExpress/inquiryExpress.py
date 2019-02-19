'''
Function:
	快递查询系统V1.0
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import sys
import pickle
import requests
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit


companies = pickle.load(open('companies.pkl', 'rb'))


'''将快递公司的拼音变为汉字'''
def py2hz(py):
	return companies.get(py)


'''利用快递100查询快递'''
def getExpressInfo(number):
	url = 'http://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text=%s' % number
	infos = []
	for each in requests.get(url).json()['auto']:
		company_name = each['comCode']
		url = 'http://www.kuaidi100.com/query?type=%s&postid=%s' % (company_name, number)
		temps = requests.get(url).json()['data']
		info = '公司: %s\n' % py2hz(company_name)
		for idx, each in enumerate(temps):
			if idx == 0:
				info += '-' * 60 + '\n时间:\n' + each['time'] + '\n进度:\n' + each['context'] + '\n' + '-' * 60 + '\n'
			else:
				info += '时间:\n' + each['time'] + '\n进度:\n' + each['context'] + '\n' + '-' * 60 + '\n'
		if not temps:
			info += '-' * 60 + '\n' + '单号不存在或已过期\n' + '-' * 60 + '\n'
		infos.append(info)
	return infos


'''实现简单的Demo'''
class Demo(QWidget):
	def __init__(self, parent=None):
		super().__init__()
		self.setWindowTitle('快递查询系统-微信公众号:Charles的皮卡丘')
		self.label1 = QLabel('快递单号:')
		self.line_edit = QLineEdit()
		self.label2 = QLabel('查询结果:')
		self.text = QTextEdit()
		self.button = QPushButton()
		self.button.setText('查询')
		self.grid = QGridLayout()
		self.grid.setSpacing(12)
		self.grid.addWidget(self.label1, 1, 0)
		self.grid.addWidget(self.line_edit, 1, 1, 1, 39)
		self.grid.addWidget(self.button, 1, 40)
		self.grid.addWidget(self.label2, 2, 0)
		self.grid.addWidget(self.text, 2, 1, 1, 40)
		self.setLayout(self.grid)
		self.resize(200, 400)
		self.button.clicked.connect(self.inquiry)
	def inquiry(self):
		number = self.line_edit.text()
		try:
			infos = getExpressInfo(number)
			if not infos:
				infos = ['-' * 60 + '\n' + '单号不存在或已过期\n' + '-' * 60 + '\n']
		except:
			infos = ['-' * 60 + '\n' + '快递单号有误, 请重新输入.\n' + '-' * 60 + '\n']
		self.text.setText('\n\n\n'.join(infos)[:-1])


if __name__ == '__main__':
	app = QApplication(sys.argv)
	demo = Demo()
	demo.show()
	sys.exit(app.exec_())