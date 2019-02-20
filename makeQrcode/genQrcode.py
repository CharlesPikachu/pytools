'''
Function:
	二维码生成器
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import io
import sys
import qrcode
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpinBox, QFileDialog, QDialog


'''Demo'''
class qrcodeGUI(QtWidgets.QWidget):
	def __init__(self, parent=None):
		super().__init__()
		self.setFixedSize(600, 400)
		self.setWindowTitle('二维码生成器-Charles的皮卡丘')
		self.grid = QGridLayout()
		# 定义组件
		# 	--Label
		self.content_label = QLabel('内容:')
		self.size_label = QLabel('尺寸:')
		self.version_label = QLabel('版本:')
		self.margin_label = QLabel('边距:')
		self.rendering_label = QLabel('效果:')
		self.show_label = QLabel()
		# 		使得图片可缩放
		self.show_label.setScaledContents(True)
		# 		显示时的最大尺寸
		self.show_label.setMaximumSize(200, 200)
		# 	--输入框
		self.content_edit = QLineEdit()
		self.content_edit.setText('微信公众号:Charles的皮卡丘')
		# 	--按钮
		self.generate_button = QPushButton('生成二维码')
		self.save_button = QPushButton('保存二维码')
		# 	--下拉框
		self.version_combobox = QComboBox()
		for i in range(1, 41):
			self.version_combobox.addItem('%s' % str(i))
		self.size_combobox = QComboBox()
		for i in range(8, 40, 2):
			self.size_combobox.addItem('%s * %s' % (str(i*29), str(i*29)))
		# 	--微调框
		self.margin_spinbox = QSpinBox()
		# 布局
		# 	数字依次对应行, 列, 行数和列数
		self.grid.addWidget(self.rendering_label, 0, 0, 1, 1)
		self.grid.addWidget(self.show_label, 0, 0, 5, 5)
		self.grid.addWidget(self.content_label, 0, 5, 1, 1)
		self.grid.addWidget(self.content_edit, 0, 6, 1, 3)
		self.grid.addWidget(self.version_label, 1, 5, 1, 1)
		self.grid.addWidget(self.version_combobox, 1, 6, 1, 1)
		self.grid.addWidget(self.size_label, 2, 5, 1, 1)
		self.grid.addWidget(self.size_combobox, 2, 6, 1, 1)
		self.grid.addWidget(self.margin_label, 3, 5, 1, 1)
		self.grid.addWidget(self.margin_spinbox, 3, 6, 1, 1)
		self.grid.addWidget(self.generate_button, 4, 5, 1, 2)
		self.grid.addWidget(self.save_button, 5, 5, 1, 2)
		self.setLayout(self.grid)
		self.generate_button.clicked.connect(self.genQrcode)
		self.save_button.clicked.connect(self.saveQrcode)
		self.margin_spinbox.valueChanged.connect(self.genQrcode)
		self.genQrcode()
	'''生成二维码'''
	def genQrcode(self):
		content = self.content_edit.text()
		try:
			margin = int(self.margin_spinbox.text())
		except:
			margin = 0
		size = int(self.size_combobox.currentText().split('*')[0])
		qr = qrcode.QRCode(version=1,
						   error_correction=qrcode.constants.ERROR_CORRECT_L,
						   box_size=size//29,
						   border=margin)
		qr.add_data(content)
		self.qr_img = qr.make_image()
		fp = io.BytesIO()
		self.qr_img.save(fp, 'BMP')
		qimg = QtGui.QImage()
		qimg.loadFromData(fp.getvalue(), 'BMP')
		qimg_pixmap = QtGui.QPixmap.fromImage(qimg)
		self.show_label.setPixmap(qimg_pixmap)
	'''保存二维码'''
	def saveQrcode(self):
		filename = QFileDialog.getSaveFileName(self, '保存', './qrcode.png', '所有文件(*)')
		if filename[0] != '':
			self.qr_img.save(filename[0])
			QDialog().show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = qrcodeGUI()
	gui.show()
	sys.exit(app.exec_())