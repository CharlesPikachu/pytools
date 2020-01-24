'''
Function:
    生成新年祝福贺卡
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import io
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
from PIL import Image, ImageDraw, ImageFont


'''生成新年祝福贺卡'''
class newyearCardGUI(QtWidgets.QWidget):
    def __init__(self):
        super(newyearCardGUI, self).__init__()
        self.setFixedSize(600, 500)
        self.setWindowTitle('新年贺卡生成器-Charles的皮卡丘')
        self.setWindowIcon(QIcon('icon/icon.png'))
        self.grid = QGridLayout()
        # 一些全局变量
        self.card_image = None
        self.font_size = 35
        # 定义组件
        # --Label
        self.content_label = QLabel('内容路径:')
        self.bg_label = QLabel('背景路径:')
        self.font_label = QLabel('字体路径:')
        self.fontcolor_label = QLabel('字体颜色:')
        self.show_label = QLabel()
        self.show_label.setScaledContents(True)
        self.show_label.setMaximumSize(600, 300)
        # --输入框
        self.content_edit = QLineEdit()
        self.content_edit.setText('contents/1.card')
        self.bg_edit = QLineEdit()
        self.bg_edit.setText('bgimages/1.png')
        self.font_edit = QLineEdit()
        self.font_edit.setText('fonts/font.TTF')
        # --按钮
        self.choose_content_button = QPushButton('选择路径')
        self.choose_bg_button = QPushButton('选择路径')
        self.choose_font_button = QPushButton('选择路径')
        self.generate_button = QPushButton('生成贺卡')
        self.save_button = QPushButton('保存贺卡')
        # --下拉框
        self.font_color_combobox = QComboBox()
        for color in ['red', 'white', 'black', 'blue', 'yellow', 'green']:
            self.font_color_combobox.addItem(color)
        # 布局
        self.grid.addWidget(self.show_label, 0, 0, 5, 5)
        self.grid.addWidget(self.content_label, 5, 0, 1, 1)
        self.grid.addWidget(self.content_edit, 5, 1, 1, 3)
        self.grid.addWidget(self.choose_content_button, 5, 4, 1, 1)
        self.grid.addWidget(self.bg_label, 6, 0, 1, 1)
        self.grid.addWidget(self.bg_edit, 6, 1, 1, 3)
        self.grid.addWidget(self.choose_bg_button, 6, 4, 1, 1)
        self.grid.addWidget(self.font_label, 7, 0, 1, 1)
        self.grid.addWidget(self.font_edit, 7, 1, 1, 3)
        self.grid.addWidget(self.choose_font_button, 7, 4, 1, 1)
        self.grid.addWidget(self.fontcolor_label, 8, 0, 1, 1)
        self.grid.addWidget(self.font_color_combobox, 8, 1, 1, 1)
        self.grid.addWidget(self.generate_button, 8, 3, 1, 1)
        self.grid.addWidget(self.save_button, 8, 4, 1, 1)
        self.setLayout(self.grid)
        # 事件绑定
        self.choose_content_button.clicked.connect(self.openContentFilepath)
        self.choose_bg_button.clicked.connect(self.openBGFilepath)
        self.choose_font_button.clicked.connect(self.openFontFilepath)
        self.generate_button.clicked.connect(self.generate)
        self.save_button.clicked.connect(self.save)
        self.generate()
    '''生成贺卡'''
    def generate(self):
        # 检查路径是否存在
        content_path = self.content_edit.text()
        bg_path = self.bg_edit.text()
        font_path = self.font_edit.text()
        font_color = self.font_color_combobox.currentText()
        if (not self.checkFilepath(content_path)) or (not self.checkFilepath(bg_path)) or (not self.checkFilepath(font_path)):
            self.card_image = None
            return False
        # 写贺卡
        contents = open(content_path, encoding='utf-8').read().split('\n')
        font_card = ImageFont.truetype(font_path, self.font_size)
        image = Image.open(bg_path).convert('RGB')
        draw = ImageDraw.Draw(image)
        draw.text((180, 30), contents[0], font=font_card, fill=font_color)
        for idx, content in enumerate(contents[1: -1]):
            draw.text((220, 40+(idx+1)*40), content, font=font_card, fill=font_color)
        draw.text((180, 40+(idx+2)*40+10), contents[-1], font=font_card, fill=font_color)
        # 显示
        fp = io.BytesIO()
        image.save(fp, 'BMP')
        qtimg = QtGui.QImage()
        qtimg.loadFromData(fp.getvalue(), 'BMP')
        qtimg_pixmap = QtGui.QPixmap.fromImage(qtimg)
        self.show_label.setPixmap(qtimg_pixmap)
        self.card_image = image
    '''打开贺卡内容文件'''
    def openContentFilepath(self):
        filepath = QFileDialog.getOpenFileName(self, "请选取贺卡内容文件", '.')
        self.content_edit.setText(filepath[0])
    '''打开贺卡背景图片文件'''
    def openBGFilepath(self):
        filepath = QFileDialog.getOpenFileName(self, "请选取贺卡背景图片", '.')
        self.bg_edit.setText(filepath[0])
    '''打开字体路径'''
    def openFontFilepath(self):
        filepath = QFileDialog.getOpenFileName(self, "请选取字体文件", '.')
        self.font_edit.setText(filepath[0])
    '''保存贺卡'''
    def save(self):
        filename = QFileDialog.getSaveFileName(self, '保存', './card.jpg', '所有文件(*)')
        if filename[0] != '' and self.card_image:
            self.card_image.save(filename[0])
            QDialog().show()
    '''检查文件是否存在'''
    def checkFilepath(self, filepath):
        if not filepath:
            return False
        return os.path.isfile(filepath)


'''run'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = newyearCardGUI()
    gui.show()
    sys.exit(app.exec_())