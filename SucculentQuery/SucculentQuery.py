'''
Function:
    多肉数据查询系统
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import io
import os
import sys
import random
import threading
from PyQt5 import *
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from modules.crawler import *
from PyQt5 import QtWidgets, QtGui


'''多肉数据查询系统'''
class SucculentQuery(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(SucculentQuery, self).__init__(parent)
        self.setWindowTitle('多肉数据查询系统-微信公众号:Charles的皮卡丘')
        self.setWindowIcon(QIcon('resources/icon/icon.png'))
        # 定义组件
        self.label_name = QLabel('多肉名称: ')
        self.line_edit = QLineEdit()
        self.button_find = QPushButton()
        self.button_find.setText('查询')
        self.label_result = QLabel('查询结果:')
        self.show_label = QLabel()
        self.show_label.setFixedSize(300, 300)
        self.showLabelImage('resources/icon/icon.png')
        self.text_result = QTextEdit()
        self.button_random = QPushButton()
        self.button_random.setText('随机读取')
        self.button_update = QPushButton()
        self.button_update.setText('数据更新')
        self.tip_label = QLabel()
        self.tip_label.setText('数据状态: 未在更新数据, 数据更新进度: 0/0')
        # 排版
        self.grid = QGridLayout()
        self.grid.addWidget(self.label_name, 0, 0, 1, 1)
        self.grid.addWidget(self.line_edit, 0, 1, 1, 30)
        self.grid.addWidget(self.button_find, 0, 31, 1, 1)
        self.grid.addWidget(self.button_random, 0, 32, 1, 1)
        self.grid.addWidget(self.button_update, 0, 33, 1, 1)
        self.grid.addWidget(self.tip_label, 1, 0, 1, 31)
        self.grid.addWidget(self.label_result, 2, 0)
        self.grid.addWidget(self.text_result, 3, 0, 1, 34)
        self.grid.addWidget(self.show_label, 3, 34, 1, 1)
        self.setLayout(self.grid)
        self.resize(600, 400)
        # 事件绑定
        self.button_find.clicked.connect(self.find)
        self.button_random.clicked.connect(self.randomRead)
        self.button_update.clicked.connect(lambda _: threading.Thread(target=self.update).start())
    '''数据查询'''
    def find(self):
        datadir = os.path.join('resources/succulents/', self.line_edit.text())
        if os.path.exists(datadir):
            self.showLabelImage(os.path.join(datadir, 'show.jpg'))
            intro = pickle.load(open(os.path.join(datadir, 'info.pkl'), 'rb'))[-1]
            self.showIntroduction(intro)
    '''随机读取'''
    def randomRead(self):
        datadir = random.choice(os.listdir('resources/succulents/'))
        self.line_edit.setText(datadir)
        datadir = os.path.join('resources/succulents/', self.line_edit.text())
        if os.path.exists(datadir):
            self.showLabelImage(os.path.join(datadir, 'show.jpg'))
            intro = pickle.load(open(os.path.join(datadir, 'info.pkl'), 'rb'))[-1]
            self.showIntroduction(intro)
    '''数据更新'''
    def update(self):
        crawler_handle = SucculentCrawler()
        while True:
            self.tip_label.setText('数据状态: 正在在更新数据, 数据更新进度: %s/%s' % (crawler_handle.page_pointer+2, len(crawler_handle.page_urls)))
            if crawler_handle.next():
                break
        self.tip_label.setText('数据状态: 未在更新数据, 数据更新进度: 0/0')
    '''在文本框里显示多肉介绍'''
    def showIntroduction(self, intro):
        self.text_result.setText('\n\n'.join(intro))
    '''在Label对象上显示图片'''
    def showLabelImage(self, imagepath):
        image = Image.open(imagepath).resize((300, 300), Image.ANTIALIAS)
        fp = io.BytesIO()
        image.save(fp, 'JPEG')
        qtimg = QtGui.QImage()
        qtimg.loadFromData(fp.getvalue(), 'JPEG')
        qtimg_pixmap = QtGui.QPixmap.fromImage(qtimg)
        self.show_label.setPixmap(qtimg_pixmap)


'''run'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    query_demo = SucculentQuery()
    query_demo.show()
    sys.exit(app.exec_())