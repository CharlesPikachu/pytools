'''
Function:
    what-did-hubble-see-on-your-birthday
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import io
import os
import sys
import warnings
import requests
import threading
from PyQt5 import *
from PIL import Image
from lxml import etree
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui
from openpyxl import load_workbook
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
warnings.filterwarnings('ignore')


'''what-did-hubble-see-on-your-birthday'''
class HubbleSeeOnBirthday(QWidget):
    update_signal = pyqtSignal(dict, name='data')
    def __init__(self, parent=None, **kwargs):
        super(HubbleSeeOnBirthday, self).__init__(parent)
        self.setFixedSize(700, 350)
        self.setWindowTitle('你生日那天的宇宙-微信公众号:Charles的皮卡丘')
        self.setWindowIcon(QIcon('resources/icon/icon.jpg'))
        # 定义组件
        # --label
        self.month_label = QLabel('出生月:')
        self.day_label = QLabel('出生日:')
        self.show_label = QLabel()
        self.show_label.setScaledContents(True)
        self.show_label.setMaximumSize(400, 300)
        self.showLabelImage(Image.open('resources/icon/icon.jpg'))
        # --显示介绍文字的text
        self.text_result = QTextEdit()
        # --日期选择下拉框
        self.month_combobox = QComboBox()
        for item in range(1, 13):
            self.month_combobox.addItem(str(item).zfill(2))
        self.day_combobox = QComboBox()
        for item in range(1, 32):
            self.day_combobox.addItem(str(item).zfill(2))
        # --按钮
        self.query_button = QPushButton()
        self.query_button.setText('查询')
        self.save_button = QPushButton()
        self.save_button.setText('保存')
        # 布局
        self.grid = QGridLayout()
        self.grid.setSpacing(12)
        self.grid.addWidget(self.show_label, 0, 0, 10, 10)
        self.grid.addWidget(self.text_result, 0, 10, 10, 10)
        self.grid.addWidget(self.month_label, 10, 0, 1, 1)
        self.grid.addWidget(self.month_combobox, 10, 1, 1, 1)
        self.grid.addWidget(self.day_label, 10, 2, 1, 1)
        self.grid.addWidget(self.day_combobox, 10, 3, 1, 1)
        self.grid.addWidget(self.query_button, 10, 10, 1, 1)
        self.grid.addWidget(self.save_button, 10, 11, 1, 1)
        self.setLayout(self.grid)
        # 事件绑定
        self.query_button.clicked.connect(lambda _: threading.Thread(target=self.query).start())
        self.save_button.clicked.connect(self.save)
        self.update_signal.connect(self.update)
        # 一些必要的变量
        self.is_querying = False
        self.full_year_data = self.loadFullYearData('resources/hubble-birthdays-full-year.xlsx')
        self.data_for_save = None
    '''查询'''
    def query(self):
        if not self.is_querying:
            self.is_querying = True
            key = self.month_combobox.currentText() + '-' + self.day_combobox.currentText()
            url = self.full_year_data.get(key)
            if url:
                headers = {
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                            'Cache-Control': 'no-cache',
                            'Connection': 'keep-alive',
                            'Cookie': '_ga=GA1.2.1134605765.1585543076; _gid=GA1.2.319198058.1585543076; JSESSIONID=A5B6D1F64BECBF2ACBFC3F61D4FE8EB5',
                            'Host': 'hubblesite.org',
                            'Pragma': 'no-cache',
                            'Sec-Fetch-Dest': 'document',
                            'Sec-Fetch-Mode': 'navigate',
                            'Sec-Fetch-Site': 'none',
                            'Sec-Fetch-User': '?1',
                            'Upgrade-Insecure-Requests': '1',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
                        }
                # 因为经常请求失败, 所以加个try块
                while True:
                    try:
                        res = requests.get(url, headers=headers)
                        break
                    except:
                        continue
                html_root = etree.HTML(res.text)
                html = html_root.xpath('//*[@id="main-content"]/section/section/div[1]/div/div/div[2]')[0].xpath('./p')
                # 提取介绍
                intro = []
                for item in html:
                    intro.append(item.xpath('text()')[0])
                # 提取图片链接并下载
                idx = -1
                while True:
                    image_url = html_root.xpath('//*[@id="main-content"]/section/section/div[1]/div/div/div[1]/div/a')[idx]
                    image_url = ('https:' + image_url.xpath('@href')[0]).replace('imgsrc.hubblesite.org/hvi', 'hubblesite.org')
                    if image_url.split('.')[-1] == 'jpg':
                        break
                    idx -= 1
                filename = 'tmp.%s' % image_url.split('.')[-1]
                while True:
                    try:
                        f = open(filename, 'wb')
                        session = requests.Session()
                        retry = Retry(connect=10000, backoff_factor=0.5)
                        adapter = HTTPAdapter(max_retries=retry)
                        session.mount('http://', adapter)
                        session.mount('https://', adapter)
                        res = session.get(image_url, headers=headers, stream=True, verify=False)
                        for chunk in res.iter_content(chunk_size=1024): f.write(chunk)
                        f.close()
                        break
                    except:
                        continue
                data = {'date': key, 'intro': intro, 'image': Image.open(filename), 'ext': image_url.split('.')[-1]}
            else:
                data = {'date': key, 'intro': ['地球上还不存在%s这个日期哦~' % key], 'image': Image.open('resources/icon/icon.jpg'), 'ext': 'jpg'}
            self.update_signal.emit(data)
            self.is_querying = False
    '''保存查询结果'''
    def save(self):
        if self.data_for_save:
            if not os.path.exists(self.data_for_save.get('date')):
                os.mkdir(self.data_for_save.get('date'))
                imagepath = os.path.join(self.data_for_save.get('date'), 'hubblesee.%s' % self.data_for_save.get('ext'))
                self.data_for_save.get('image').save(imagepath)
                intro = '\n\n'.join(self.data_for_save.get('intro'))
                f = open(os.path.join(self.data_for_save.get('date'), 'intro.txt'), 'w', encoding='utf-8')
                f.write(intro)
                f.close()
            self.data_for_save = None
    '''更新界面'''
    def update(self, data):
        self.showIntroduction(data.get('intro'))
        self.showLabelImage(data.get('image'))
        self.data_for_save = data
    '''导入excel中的全年数据'''
    def loadFullYearData(self, filepath):
        full_year_data = {}
        excel_data = load_workbook(filepath)
        sheet = excel_data.get_sheet_by_name('365')
        for idx, row in enumerate(sheet.rows):
            if idx > 366: break
            if idx > 0: full_year_data[row[0].value.strftime('%Y-%m-%d')[5:]] = row[4].value
        return full_year_data
    '''显示图片'''
    def showLabelImage(self, image):
        image = image.resize((400, 300), Image.ANTIALIAS)
        fp = io.BytesIO()
        image.save(fp, 'BMP')
        qtimg = QtGui.QImage()
        qtimg.loadFromData(fp.getvalue(), 'BMP')
        qtimg_pixmap = QtGui.QPixmap.fromImage(qtimg)
        self.show_label.setPixmap(qtimg_pixmap)
    '''显示介绍的文字'''
    def showIntroduction(self, intro):
        self.text_result.setText('\n\n'.join(intro))


'''run'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = HubbleSeeOnBirthday()
    gui.show()
    sys.exit(app.exec_())