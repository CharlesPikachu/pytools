'''
Function:
	音乐播放器
Author:
	Charles
'''
import os
import sys
import time
import random
import configparser
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *


'''音乐播放器'''
class musicPlayer(QWidget):
	def __init__(self):
		super().__init__()
		self.__initialize()
	'''初始化'''
	def __initialize(self):
		self.setWindowTitle('音乐播放器v0.1.0-Charles的皮卡丘')
		self.setWindowIcon(QIcon('icon.ico'))
		self.songs_list = []
		self.song_formats = ['mp3', 'm4a', 'flac', 'wav', 'ogg']
		self.settingfilename = 'setting.ini'
		self.player = QMediaPlayer()
		self.cur_path = os.path.abspath(os.path.dirname(__file__))
		self.cur_playing_song = ''
		self.is_switching = False
		self.is_pause = True
		# 界面元素
		# --播放时间
		self.label1 = QLabel('00:00')
		self.label1.setStyle(QStyleFactory.create('Fusion'))
		self.label2 = QLabel('00:00')
		self.label2.setStyle(QStyleFactory.create('Fusion'))
		# --滑动条
		self.slider = QSlider(Qt.Horizontal, self)
		self.slider.sliderMoved[int].connect(lambda: self.player.setPosition(self.slider.value()))
		self.slider.setStyle(QStyleFactory.create('Fusion'))
		# --播放按钮
		self.play_button = QPushButton('播放', self)
		self.play_button.clicked.connect(self.playMusic)
		self.play_button.setStyle(QStyleFactory.create('Fusion'))
		# --上一首按钮
		self.preview_button = QPushButton('上一首', self)
		self.preview_button.clicked.connect(self.previewMusic)
		self.preview_button.setStyle(QStyleFactory.create('Fusion'))
		# --下一首按钮
		self.next_button = QPushButton('下一首', self)
		self.next_button.clicked.connect(self.nextMusic)
		self.next_button.setStyle(QStyleFactory.create('Fusion'))
		# --打开文件夹按钮
		self.open_button = QPushButton('打开文件夹', self)
		self.open_button.setStyle(QStyleFactory.create('Fusion'))
		self.open_button.clicked.connect(self.openDir)
		# --显示音乐列表
		self.qlist = QListWidget()
		self.qlist.itemDoubleClicked.connect(self.doubleClicked)
		self.qlist.setStyle(QStyleFactory.create('windows'))
		# --如果有初始化setting, 导入setting
		self.loadSetting()
		# --播放模式
		self.cmb = QComboBox()
		self.cmb.setStyle(QStyleFactory.create('Fusion'))
		self.cmb.addItem('顺序播放')
		self.cmb.addItem('单曲循环')
		self.cmb.addItem('随机播放')
		# --计时器
		self.timer = QTimer(self)
		self.timer.start(1000)
		self.timer.timeout.connect(self.playByMode)
		# 界面布局
		self.grid = QGridLayout()
		self.setLayout(self.grid)
		self.grid.addWidget(self.qlist, 0, 0, 5, 10)
		self.grid.addWidget(self.label1, 0, 11, 1, 1)
		self.grid.addWidget(self.slider, 0, 12, 1, 1)
		self.grid.addWidget(self.label2, 0, 13, 1, 1)
		self.grid.addWidget(self.play_button, 0, 14, 1, 1)
		self.grid.addWidget(self.next_button, 1, 11, 1, 2)
		self.grid.addWidget(self.preview_button, 2, 11, 1, 2)
		self.grid.addWidget(self.cmb, 3, 11, 1, 2)
		self.grid.addWidget(self.open_button, 4, 11, 1, 2)
	'''根据播放模式播放音乐'''
	def playByMode(self):
		if (not self.is_pause) and (not self.is_switching):
			self.slider.setMinimum(0)
			self.slider.setMaximum(self.player.duration())
			self.slider.setValue(self.slider.value() + 1000)
		self.label1.setText(time.strftime('%M:%S', time.localtime(self.player.position()/1000)))
		self.label2.setText(time.strftime('%M:%S', time.localtime(self.player.duration()/1000)))
		# 顺序播放
		if (self.cmb.currentIndex() == 0) and (not self.is_pause) and (not self.is_switching):
			if self.qlist.count() == 0:
				return
			if self.player.position() == self.player.duration():
				self.nextMusic()
		# 单曲循环
		elif (self.cmb.currentIndex() == 1) and (not self.is_pause) and (not self.is_switching):
			if self.qlist.count() == 0:
				return
			if self.player.position() == self.player.duration():
				self.is_switching = True
				self.setCurPlaying()
				self.slider.setValue(0)
				self.playMusic()
				self.is_switching = False
		# 随机播放
		elif (self.cmb.currentIndex() == 2) and (not self.is_pause) and (not self.is_switching):
			if self.qlist.count() == 0:
				return
			if self.player.position() == self.player.duration():
				self.is_switching = True
				self.qlist.setCurrentRow(random.randint(0, self.qlist.count()-1))
				self.setCurPlaying()
				self.slider.setValue(0)
				self.playMusic()
				self.is_switching = False
	'''打开文件夹'''
	def openDir(self):
		self.cur_path = QFileDialog.getExistingDirectory(self, "选取文件夹", self.cur_path)
		if self.cur_path:
			self.showMusicList()
			self.cur_playing_song = ''
			self.setCurPlaying()
			self.label1.setText('00:00')
			self.label2.setText('00:00')
			self.slider.setSliderPosition(0)
			self.is_pause = True
			self.play_button.setText('播放')
	'''导入setting'''
	def loadSetting(self):
		if os.path.isfile(self.settingfilename):
			config = configparser.ConfigParser()
			config.read(self.settingfilename)
			self.cur_path = config.get('MusicPlayer', 'PATH')
			self.showMusicList()
	'''更新setting'''
	def updateSetting(self):
		config = configparser.ConfigParser()
		config.read(self.settingfilename)
		if not os.path.isfile(self.settingfilename):
			config.add_section('MusicPlayer')
		config.set('MusicPlayer', 'PATH', self.cur_path)
		config.write(open(self.settingfilename, 'w'))
	'''显示文件夹中所有音乐'''
	def showMusicList(self):
		self.qlist.clear()
		self.updateSetting()
		for song in os.listdir(self.cur_path):
			if song.split('.')[-1] in self.song_formats:
				self.songs_list.append([song, os.path.join(self.cur_path, song).replace('\\', '/')])
				self.qlist.addItem(song)
		self.qlist.setCurrentRow(0)
		if self.songs_list:
			self.cur_playing_song = self.songs_list[self.qlist.currentRow()][-1]
	'''双击播放音乐'''
	def doubleClicked(self):
		self.slider.setValue(0)
		self.is_switching = True
		self.setCurPlaying()
		self.playMusic()
		self.is_switching = False
	'''设置当前播放的音乐'''
	def setCurPlaying(self):
		self.cur_playing_song = self.songs_list[self.qlist.currentRow()][-1]
		self.player.setMedia(QMediaContent(QUrl(self.cur_playing_song)))
	'''提示'''
	def Tips(self, message):
		QMessageBox.about(self, "提示", message)
	'''播放音乐'''
	def playMusic(self):
		if self.qlist.count() == 0:
			self.Tips('当前路径内无可播放的音乐文件')
			return
		if not self.player.isAudioAvailable():
			self.setCurPlaying()
		if self.is_pause or self.is_switching:
			self.player.play()
			self.is_pause = False
			self.play_button.setText('暂停')
		elif (not self.is_pause) and (not self.is_switching):
			self.player.pause()
			self.is_pause = True
			self.play_button.setText('播放')
	'''上一首'''
	def previewMusic(self):
		self.slider.setValue(0)
		if self.qlist.count() == 0:
			self.Tips('当前路径内无可播放的音乐文件')
			return
		pre_row = self.qlist.currentRow()-1 if self.qlist.currentRow() != 0 else self.qlist.count() - 1
		self.qlist.setCurrentRow(pre_row)
		self.is_switching = True
		self.setCurPlaying()
		self.playMusic()
		self.is_switching = False
	'''下一首'''
	def nextMusic(self):
		self.slider.setValue(0)
		if self.qlist.count() == 0:
			self.Tips('当前路径内无可播放的音乐文件')
			return
		next_row = self.qlist.currentRow()+1 if self.qlist.currentRow() != self.qlist.count()-1 else 0
		self.qlist.setCurrentRow(next_row)
		self.is_switching = True
		self.setCurPlaying()
		self.playMusic()
		self.is_switching = False


'''run'''
if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = musicPlayer()
	gui.show()
	sys.exit(app.exec_())