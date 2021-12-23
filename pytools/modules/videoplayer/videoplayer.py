'''
Function:
    视频播放器
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


'''视频播放器'''
class VideoPlayer(QWidget):
    tool_name = '视频播放器'
    def __init__(self, parent=None, title='视频播放器 —— Charles的皮卡丘', **kwargs):
        super(VideoPlayer, self).__init__(parent)
        rootdir = os.path.split(os.path.abspath(__file__))[0]
        self.rootdir = rootdir
        # 初始化窗口
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(os.path.join(rootdir, 'resources/icon.png')))
        self.setGeometry(300, 50, 810, 600)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        palette = QPalette()  
        palette.setColor(QPalette.Background, Qt.gray)
        self.setPalette(palette)
        # 定义组件
        # --视频播放插件
        self.video_widget = QVideoWidget(self)
        self.video_widget.setGeometry(QRect(5, 5, 800, 520))
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.black)
        self.video_widget.setPalette(palette)
        self.video_widget.setStyleSheet('background-color:#000000')
        self.player = QMediaPlayer(self)
        self.player.setVideoOutput(self.video_widget)
        self.player.setVolume(50)
        # --当前的视频路径
        self.video_line_edit = QLineEdit('')
        # --选择视频按钮
        self.select_video_btn = QPushButton('选择')
        # --播放按钮
        self.play_btn = QPushButton(self)
        self.play_btn.setIcon(QIcon(os.path.join(rootdir, 'resources/play.png')))
        self.play_btn.setIconSize(QSize(25, 25))
        self.play_btn.setStyleSheet('''QPushButton{border:none;}QPushButton:hover{border:none;border-radius:35px;}''')
        self.play_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.play_btn.setToolTip('播放')
        self.play_btn.setFlat(True)
        # --暂停按钮
        self.pause_btn = QPushButton('')
        self.pause_btn.setIcon(QIcon(os.path.join(rootdir, 'resources/pause.png')))
        self.pause_btn.setIconSize(QSize(25, 25))
        self.pause_btn.setStyleSheet('''QPushButton{border:none;}QPushButton:hover{border:none;}''')
        self.pause_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.pause_btn.setToolTip('暂停')
        self.pause_btn.setFlat(True)
        self.pause_btn.hide()
        # --播放进度
        self.play_progress_label = QLabel('00:00 / 00: 00')
        self.play_progress_slider = QSlider(Qt.Horizontal, self)
        self.play_progress_slider.setMinimum(0)
        self.play_progress_slider.setSingleStep(1)
        self.play_progress_slider.setGeometry(QRect(0, 0, 200, 10))
        # --音量控制
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.mute_btn = QPushButton('')
        self.mute_btn.setIcon(QIcon(os.path.join(rootdir, 'resources/sound.png')))
        self.mute_btn.setIconSize(QSize(25, 25))
        self.mute_btn.setStyleSheet('''QPushButton{border:none;}QPushButton:hover{border:none;}''')
        self.mute_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.mute_btn.setToolTip('禁音')
        self.mute_btn.setFlat(True)
        self.volume_label = QLabel('50')
        # --布局
        v_layout = QVBoxLayout()
        v_layout.setSpacing(0)
        v_layout.addStretch()
        h_layout = QHBoxLayout()
        h_layout.setSpacing(15)
        h_layout.addWidget(self.video_line_edit, 2, Qt.AlignVCenter | Qt.AlignVCenter)
        h_layout.addWidget(self.select_video_btn, 0, Qt.AlignCenter | Qt.AlignVCenter)
        v_layout.addLayout(h_layout)
        h_layout = QHBoxLayout()
        h_layout.setSpacing(2)
        h_layout.addWidget(self.play_btn, 0, Qt.AlignCenter | Qt.AlignVCenter)
        h_layout.addWidget(self.pause_btn, 0, Qt.AlignCenter | Qt.AlignVCenter)
        h_layout.addWidget(self.play_progress_label, 0, Qt.AlignCenter | Qt.AlignVCenter)
        h_layout.addWidget(self.play_progress_slider, 15, Qt.AlignVCenter | Qt.AlignVCenter)
        h_layout.addWidget(self.mute_btn, 0, Qt.AlignCenter | Qt.AlignVCenter)
        h_layout.addWidget(self.volume_slider, 0, Qt.AlignCenter | Qt.AlignVCenter)
        h_layout.addWidget(self.volume_label, 0, Qt.AlignCenter | Qt.AlignVCenter)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)
        # 事件绑定
        self.player.durationChanged.connect(self.setVideoLength)
        self.player.positionChanged.connect(self.setPlayProgress)
        self.select_video_btn.clicked.connect(self.openvideo)
        self.play_btn.clicked.connect(self.playvideo)
        self.pause_btn.clicked.connect(self.pausevideo)
        self.mute_btn.clicked.connect(self.mute)
        self.volume_slider.valueChanged.connect(self.setVolume)
        self.play_progress_slider.sliderPressed.connect(self.playProgressSliderPressed)
        self.play_progress_slider.sliderReleased.connect(self.playProgressSliderReleased)
    '''播放进度条按下ing事件'''
    def playProgressSliderPressed(self):
        if self.player.state() != 0: self.player.pause()
    '''播放进度条按下释放事件'''
    def playProgressSliderReleased(self):
        if self.player.state() != 0:
            self.player.setPosition(self.play_progress_slider.value())
            self.player.play()
    '''播放视频'''
    def playvideo(self):
        if self.player.duration() == 0: return
        self.play_btn.hide()
        self.pause_btn.show()
        self.player.play()
    '''暂停视频'''
    def pausevideo(self):
        if self.player.duration() == 0: return
        self.play_btn.show()
        self.pause_btn.hide()
        self.player.pause()
    '''禁音'''
    def mute(self):
        if self.player.isMuted():
            self.mute_btn.setIcon(QIcon(os.path.join(self.rootdir, 'resources/sound.png')))
            self.player.setMuted(False)
            self.volume_label.setText('50')
            self.volume_slider.setValue(50)
            self.player.setVolume(50)
        else:
            self.player.setMuted(True)
            self.volume_label.setText('0')
            self.volume_slider.setValue(0)
            self.mute_btn.setIcon(QIcon(os.path.join(self.rootdir, 'resources/mute.png')))
    '''打开视频文件'''
    def openvideo(self):
        # 打开并显示视频路径
        filepath = QFileDialog.getOpenFileName(self, '请选择视频', '.')
        if filepath[0]:
            self.video_line_edit.setText(filepath[0])
        # 将视频路径初始化进视频播放插件
        filepath = self.video_line_edit.text()
        if not os.path.exists(filepath): return
        fileurl = QUrl.fromLocalFile(filepath)
        if fileurl.isValid():
            self.player.setMedia(QMediaContent(fileurl))
            self.player.setVolume(50)
    '''设置音量'''
    def setVolume(self):
        value = self.volume_slider.value()
        if value:
            self.player.setMuted(False)
            self.player.setVolume(value)
            self.volume_label.setText(str(value))
            self.volume_slider.setValue(value)
            self.mute_btn.setIcon(QIcon(os.path.join(self.rootdir, 'resources/sound.png')))
        else:
            self.player.setMuted(True)
            self.volume_label.setText('0')
            self.volume_slider.setValue(0)
            self.mute_btn.setIcon(QIcon(os.path.join(self.rootdir, 'resources/mute.png')))
    '''播放进度设置'''
    def setPlayProgress(self):
        _, right = self.play_progress_label.text().split('/')
        position = self.player.position() + 1
        second = int(position / 1000 % 60)
        minute = int(position / 1000 / 60)
        left = str(minute).zfill(2) + ':' + str(second).zfill(2)
        self.play_progress_label.setText(left + ' /' + right)
        self.play_progress_slider.setValue(position)
    '''视频时长显示更改'''
    def setVideoLength(self):
        left, _ = self.play_progress_label.text().split('/')
        duration = self.player.duration()
        self.play_progress_slider.setMaximum(duration)
        second = int(duration / 1000 % 60)
        minute = int(duration / 1000 / 60)
        right = str(minute).zfill(2) + ':' + str(second).zfill(2)
        self.play_progress_label.setText(left + '/ ' + right)
    '''关闭窗口'''
    def closeEvent(self, event):
        self.player.stop()
    '''改变窗口大小'''
    def resizeEvent(self, event):
        size = event.size()
        self.video_widget.setGeometry(5, 5, size.width() - 5, size.height() - 80)