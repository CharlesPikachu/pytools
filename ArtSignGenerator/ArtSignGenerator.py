'''
Function:
    艺术签名生成器
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import re
import io
import sys
import requests
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui


'''艺术签名生成器'''
class ArtSignGenerator(QWidget):
    def __init__(self, parent=None):
        super(ArtSignGenerator, self).__init__(parent)
        self.setFixedSize(600, 500)
        self.setWindowTitle('艺术签名生成器-Charles的皮卡丘')
        self.setWindowIcon(QIcon('resource/icon/icon.jpg'))
        self.grid = QGridLayout()
        # 定义一些必要的组件
        # --label
        self.show_label = QLabel()
        self.show_label.setScaledContents(True)
        self.show_label.setMaximumSize(600, 400)
        self.show_image = Image.open('resource/image/ori.jpg').convert('RGB')
        self.updateimage()
        self.show_image_ext = 'jpg'
        self.name_label = QLabel('输入您的姓名:')
        self.font_label = QLabel('艺术签名字体:')
        self.color_label = QLabel('艺术签名颜色:')
        # --输入框
        self.name_edit = QLineEdit()
        self.name_edit.setText('签名生成器')
        # --button
        self.generate_button = QPushButton('生成艺术签名')
        self.save_button = QPushButton('保存艺术签名')
        # --下拉框
        self.font_combobox = QComboBox()
        for item in ['一笔艺术签', '连笔商务签', '一笔商务签', '真人手写', '暴躁字']:
            self.font_combobox.addItem(item)
        self.color_combobox = QComboBox()
        for item in ['Black', 'Blue', 'Red', 'Green', 'Yellow', 
                     'Pink', 'DeepSkyBlue', 'Cyan', 'Orange', 'Seashell']:
            self.color_combobox.addItem(item)
        # 组件布局
        self.grid.addWidget(self.show_label, 0, 0, 5, 5)
        self.grid.addWidget(self.name_label, 5, 0, 1, 1)
        self.grid.addWidget(self.name_edit, 5, 1, 1, 4)
        self.grid.addWidget(self.font_label, 6, 0, 1, 1)
        self.grid.addWidget(self.font_combobox, 6, 1, 1, 4)
        self.grid.addWidget(self.color_label, 7, 0, 1, 1)
        self.grid.addWidget(self.color_combobox, 7, 1, 1, 4)
        self.grid.addWidget(self.generate_button, 8, 3, 1, 1)
        self.grid.addWidget(self.save_button, 8, 4, 1, 1)
        self.setLayout(self.grid)
        # 事件绑定
        self.generate_button.clicked.connect(self.generate)
        self.save_button.clicked.connect(self.save)
    '''生成签名'''
    def generate(self):
        font2ids_dict = {
                            '一笔艺术签': ['901', '15'],
                            '连笔商务签': ['904', '15'],
                            '一笔商务签': ['905', '14'],
                            '真人手写': ['343', '14'],
                            '卡通趣圆字': ['397', '14'],
                            '暴躁字': ['380', '14']
                    }
        color2ids_dict = {
                            'Black': ['#000000', '#FFFFFF'],
                            'Blue': ['#0000FF', '#FFFFFF'],
                            'Red': ['#FF0000', '#FFFFFF'],
                            'Green': ['#00FF00', '#FFFFFF'],
                            'Yellow': ['#FFFF00', '#FFFFFF'],
                            'Pink': ['#FFC0CB', '#FFFFFF'],
                            'DeepSkyBlue': ['#00BFFF', '#FFFFFF'],
                            'Cyan': ['#00FFFF', '#FFFFFF'],
                            'Orange': ['#FFA500', '#FFFFFF'],
                            'Seashell': ['#FFF5EE', '#FFFFFF']
                        }
        url = 'http://www.jiqie.com/a/re14.php'
        headers = {
                    'Referer': 'http://www.jiqie.com/a/14.htm',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
                    'Host': 'www.jiqie.com',
                    'Origin': 'http://www.jiqie.com'
                }
        ids_0 = font2ids_dict[self.font_combobox.currentText()]
        ids_1 = color2ids_dict[self.color_combobox.currentText()]
        data = {
                    'id': self.name_edit.text(),
                    'zhenbi': '20191123',
                    'id1': ids_0[0],
                    'id2': ids_0[1],
                    'id3': ids_1[0],
                    'id5': ids_1[1]
                }
        res = requests.post(url, headers=headers, data=data)
        image_url = re.findall(r'src="(.*?)"', res.text)[0]
        self.show_image_ext = image_url.split('.')[-1].split('?')[0]
        res = requests.get(image_url)
        fp = open('tmp.%s' % self.show_image_ext, 'wb')
        fp.write(res.content)
        fp.close()
        self.show_image = Image.open('tmp.%s' % self.show_image_ext).convert('RGB')
        self.updateimage()
        os.remove('tmp.%s' % self.show_image_ext)
    '''更新界面上的图片'''
    def updateimage(self):
        if self.show_image is None:
            return
        fp = io.BytesIO()
        self.show_image.save(fp, 'JPEG')
        qtimage = QtGui.QImage()
        qtimage.loadFromData(fp.getvalue(), 'JPEG')
        qtimage_pixmap = QtGui.QPixmap.fromImage(qtimage)
        self.show_label.setPixmap(qtimage_pixmap)
    '''保存签名'''
    def save(self):
        if self.show_image is None:
            return
        filename = QFileDialog.getSaveFileName(self, '保存', './sign.%s' % self.show_image_ext, '所有文件(*)')
        if filename[0]:
            self.show_image.save(filename[0])
            QDialog().show()


'''run'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ArtSignGenerator()
    gui.show()
    sys.exit(app.exec_())