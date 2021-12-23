'''
Function:
    成语接龙小软件
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import random
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


'''成语接龙'''
class IdiomSolitaire(QWidget):
    tool_name = '成语接龙小软件'
    def __init__(self, parent=None, title='成语接龙小软件 —— Charles的皮卡丘', **kwargs):
        super(IdiomSolitaire, self).__init__(parent)
        rootdir = os.path.split(os.path.abspath(__file__))[0]
        # 读取数据
        self.idiom_data, self.valid_idioms = self.readData(os.path.join(rootdir, 'resources/data.txt'))
        self.ai_answer = None
        # 定义界面
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(os.path.join(rootdir, 'resources/icon.jpg')))
        self.setFixedSize(600, 200)
        self.user_input_label = QLabel('我方:')
        self.user_input_edit = QLineEdit()
        self.user_input_button = QPushButton('确定')
        self.ai_input_label = QLabel('电脑方:')
        self.ai_input_edit = QLineEdit()
        self.restart_button = QPushButton('重新开始')
        self.user_explain_label = QLabel('我方成语释义:')
        self.user_explain_edit = QLineEdit()
        self.ai_explain_label = QLabel('电脑方成语释义:')
        self.ai_explain_edit = QLineEdit()
        # 布局
        self.grid = QGridLayout()
        self.grid.setSpacing(12)
        self.grid.addWidget(self.user_input_label, 0, 0)
        self.grid.addWidget(self.user_input_edit, 0, 1)
        self.grid.addWidget(self.user_input_button, 0, 2)
        self.grid.addWidget(self.user_explain_label, 1, 0)
        self.grid.addWidget(self.user_explain_edit, 1, 1, 1, 2)
        self.grid.addWidget(self.ai_input_label, 2, 0)
        self.grid.addWidget(self.ai_input_edit, 2, 1)
        self.grid.addWidget(self.restart_button, 2, 2)
        self.grid.addWidget(self.ai_explain_label, 3, 0)
        self.grid.addWidget(self.ai_explain_edit, 3, 1, 1, 2)
        self.setLayout(self.grid)
        # 按键绑定
        self.user_input_button.clicked.connect(self.airound)
        self.restart_button.clicked.connect(self.restart)
    '''电脑接龙'''
    def airound(self):
        idiom = self.user_input_edit.text()
        idiom = idiom.strip()
        if (not self.isvalid(idiom)) or (self.ai_answer and idiom[0] != self.ai_answer[0][-1]):
            QMessageBox.warning(self, '成语输入错误', '你输入的成语不对哦, 不可以耍小聪明哒!', QMessageBox.Yes | QMessageBox.No)
        else:
            self.user_explain_edit.setText('读音: %s; 含义: %s' % (self.valid_idioms[idiom][0], self.valid_idioms[idiom][1]))
            if idiom[-1] in self.idiom_data:
                answers = self.idiom_data[idiom[-1]]
                answer = random.choice(answers)
                self.ai_answer = answer.copy()
                self.ai_input_edit.setText(self.ai_answer[0])
                self.ai_explain_edit.setText('读音: %s; 含义: %s' % (self.valid_idioms[answer[0]][0], self.valid_idioms[answer[0]][1]))
            else:
                QMessageBox.information(self, '你赢啦', '电脑都接不上你的成语, 你太厉害啦!', QMessageBox.Yes | QMessageBox.No)
    '''重新开始'''
    def restart(self):
        self.ai_answer = None
        self.ai_input_edit.clear()
        self.ai_explain_edit.clear()
        self.user_input_edit.clear()
        self.user_explain_edit.clear()
    '''检测成语是否合法'''
    def isvalid(self, idiom):
        return (idiom in self.valid_idioms)
    '''读取成语数据'''
    def readData(self, filepath):
        fp = open(filepath, 'r', encoding='utf-8')
        idiom_data = {}
        valid_idioms = {}
        for line in fp.readlines():
            line = line.strip()
            if not line: continue
            item = line.split('\t')
            if len(item) != 3: continue
            if item[0][0] not in idiom_data:
                idiom_data[item[0][0]] = [item]
            else:
                idiom_data[item[0][0]].append(item)
            valid_idioms[item[0]] = item[1:]
        return idiom_data, valid_idioms