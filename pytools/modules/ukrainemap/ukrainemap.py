'''
Function:
    乌克兰地图查询系统
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import io
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong']


'''乌克兰地图查询系统'''
class UkraineMap(QWidget):
    tool_name = '乌克兰地图查询系统'
    def __init__(self, parent=None, title='乌克兰地图查询系统 —— Charles的皮卡丘', **kwargs):
        super(UkraineMap, self).__init__(parent)
        # 文件路径初始化
        self.rootdir = os.path.split(os.path.abspath(__file__))[0]
        self.mapdir = os.path.join(self.rootdir, 'resources')
        # 获得所有州的中英文名
        filenames, self.en2cn_states, self.cn2en_states, self.cn2color_states = os.listdir(self.mapdir), {}, {}, {}
        palettes = self.generatepalette(len(filenames))
        for idx, filename in enumerate(filenames):
            state_en = filename.split('.')[0]
            if state_en == 'Ukraine': continue
            info = json.load(open(os.path.join(self.mapdir, filename), 'r', encoding='utf-8'))
            try:
                state_cn = info['properties']['name:zh']
            except:
                if info['properties']['name:en'] == 'Autonomous Republic of Crimea':
                    state_cn = '克里米亚'
            self.en2cn_states[state_en] = state_cn
            self.cn2en_states[state_cn] = state_en
            self.cn2color_states[state_cn] = self.rgb2hex(tuple(palettes[idx]))
        # 窗口初始化
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(os.path.join(self.rootdir, 'icon.png')))
        self.setFixedSize(660, 550)
        # 定义组件
        self.map_type_label = QLabel('目前显示的乌克兰地图类型: ')
        self.show_label = QLabel()
        self.show_label.setFixedSize(640, 480)
        self.drawukraine()
        self.map_items = QComboBox()
        self.map_items.addItem('乌克兰地图-基础')
        for name in self.cn2color_states: self.map_items.addItem(f'乌克兰地图-{name}')
        self.select_btn = QPushButton('绘制')
        # 排版
        grid = QGridLayout()
        grid.addWidget(self.map_type_label, 0, 0, 1, 1)
        grid.addWidget(self.show_label, 1, 0, 1, 3)
        grid.addWidget(self.map_items, 0, 1, 1, 1)
        grid.addWidget(self.select_btn, 0, 2, 1, 1)
        self.setLayout(grid)
        # 事件绑定
        self.select_btn.clicked.connect(self.draw)
    '''在Label对象上显示图片'''
    def showLabelImage(self, imagepath):
        image = Image.open(imagepath).resize((640, 480), Image.ANTIALIAS)
        fp = io.BytesIO()
        image.save(fp, 'PNG')
        qtimg = QtGui.QImage()
        qtimg.loadFromData(fp.getvalue(), 'PNG')
        qtimg_pixmap = QtGui.QPixmap.fromImage(qtimg)
        self.show_label.setPixmap(qtimg_pixmap)
    '''生成颜色'''
    def generatepalette(self, num_classes):
        palette = [0] * (num_classes * 3)
        for j in range(0, num_classes):
            lab = j
            palette[j * 3 + 0] = 0
            palette[j * 3 + 1] = 0
            palette[j * 3 + 2] = 0
            i = 0
            while lab:
                palette[j * 3 + 0] |= (((lab >> 0) & 1) << (7 - i))
                palette[j * 3 + 1] |= (((lab >> 1) & 1) << (7 - i))
                palette[j * 3 + 2] |= (((lab >> 2) & 1) << (7 - i))
                i += 1
                lab >>= 3
        palette = np.array(palette).reshape(-1, 3)
        palette = palette.tolist()
        return palette
    '''rgb转16进制'''
    def rgb2hex(self, rgb):
        color = '#'
        for num in rgb:
            color += str(hex(num))[-2:].replace('x', '0').upper()
        return color
    '''绘制'''
    def draw(self):
        state_name_cn = '-'.join(self.map_items.currentText().split('-')[1:])
        if state_name_cn == '基础':
            self.drawukraine()
        else:
            self.drawstate(self.cn2en_states[state_name_cn], self.cn2color_states[state_name_cn])
    '''画乌克兰'''
    def drawukraine(self, show_label_image=True):
        info = json.load(open(os.path.join(self.mapdir, 'Ukraine.json'), 'r', encoding='utf-8'))
        features = info['features']
        for feature in features:
            try:
                state_cn = feature['properties']['name:zh']
            except:
                if feature['properties']['name:en'] == 'Autonomous Republic of Crimea':
                    state_cn = '克里米亚'
            geometry = feature['geometry']
            x_list, y_list = [], []
            for coordinate in geometry['coordinates'][-1]:
                if not coordinate: continue
                x_list.append(coordinate[0])
                y_list.append(coordinate[1])
            plt.plot(x_list, y_list, color='black')
        if show_label_image: 
            plt.savefig(os.path.join(self.rootdir, 'ukraine.png'))
            plt.close()
            self.showLabelImage(os.path.join(self.rootdir, 'ukraine.png'))
    '''画乌克兰的某个州'''
    def drawstate(self, state_name='Kiev', color=None):
        assert state_name in self.en2cn_states
        self.drawukraine(show_label_image=False)
        info = json.load(open(os.path.join(self.mapdir, state_name+'.json'), 'r', encoding='utf-8'))
        geometry = info['geometry']
        x_list, y_list = [], []
        for coordinate in geometry['coordinates'][-1]:
            if not coordinate: continue
            x_list.append(coordinate[0])
            y_list.append(coordinate[1])
            plt.plot(x_list, y_list, color=color)
            plt.text(x_list[0], y_list[0], self.en2cn_states[state_name], size=10, color=color)
        plt.savefig(os.path.join(self.rootdir, f'{state_name}.png'))
        plt.close()
        self.showLabelImage(os.path.join(self.rootdir, f'{state_name}.png'))