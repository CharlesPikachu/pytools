'''
Function:
    桌面宠物
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import sys
import time
import random
import requests
import threading
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtGui


'''配置信息'''
class Config():
    ROOT_DIR = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'resources')
    ACTION_DISTRIBUTION = [
        ['1', '2', '3'],
        ['4', '5', '6', '7', '8', '9', '10', '11'],
        ['12', '13', '14'],
        ['15', '16', '17'],
        ['18', '19'],
        ['20', '21'],
        ['22'],
        ['23', '24', '25'],
        ['26',  '27', '28', '29'],
        ['30', '31', '32', '33'],
        ['34', '35', '36', '37'],
        ['38', '39', '40', '41'],
        ['42', '43', '44', '45', '46']
    ]
    PET_ACTIONS_MAP = dict()
    for name in ['pikachu', 'blackcat', 'whitecat', 'fox']:
        PET_ACTIONS_MAP[name] = ACTION_DISTRIBUTION
    PET_ACTIONS_MAP['bingdwendwen'] = [
        [str(i) for i in range(1, 41, 8)],
        [str(i) for i in range(41, 56)],
        [str(i) for i in range(56, 91)],
    ]
    BAIDU_KEYS = random.choice([
        ['25419425', 'fct6UMiQMLsp53MqXzp7AbKQ', 'p3wU9nPnfR7iBz2kM25sikN2ms0y84T3'],
        ['24941009', '2c5AnnNaQKOIcTrLDTuY41vv', 'HOYo7BunbFtt88Z0ALFZcFSQ4ZVyIgiZ'],
        ['11403041', 'swB03t9EbokK03htGsg0PKYe', 'XX20l47se2tSGmet8NihkHQLIjTIHUyy'],
    ])


'''语音识别模块'''
class SpeechRecognition():
    def __init__(self, app_id, api_key, secret_key, **kwargs):
        from aip import AipSpeech
        self.aipspeech_api = AipSpeech(app_id, api_key, secret_key)
        self.speech_path = kwargs.get('speech_path', 'recording.wav')
        assert self.speech_path.endswith('.wav'), 'only support audio with wav format'
    '''录音'''
    def record(self, sample_rate=16000):
        import speech_recognition as sr
        rec = sr.Recognizer()
        with sr.Microphone(sample_rate=sample_rate) as source:
            audio = rec.listen(source)
        with open(self.speech_path, 'wb') as fp:
            fp.write(audio.get_wav_data())
    '''识别'''
    def recognition(self):
        try:
            assert os.path.exists(self.speech_path)
            with open(self.speech_path, 'rb') as fp:
                content = fp.read()
            result = self.aipspeech_api.asr(content, 'wav', 16000, {'dev_pid': 1536})
            text = result['result'][0]
            return text
        except:
            return None
    '''合成并说话'''
    def synthesisspeak(self, text=None, audiopath=None):
        assert text is None or audiopath is None
        import pygame
        if audiopath is None:
            audiopath = f'recording_{time.time()}.mp3'
            result = self.aipspeech_api.synthesis(
                text, 'zh', 1, 
                {'spd': 4, 'vol': 5, 'per': 4}
            )
            if not isinstance(result, dict):
                with open(audiopath, 'wb') as fp:
                    fp.write(result)
            pygame.mixer.init()
            pygame.mixer.music.load(audiopath)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.5)
        else:
            pygame.mixer.init()
            pygame.mixer.music.load(audiopath)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.5)


'''桌面宠物'''
class DesktopPet(QWidget):
    tool_name = '桌面宠物'
    def __init__(self, pet_type='pikachu', parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        self.pet_type = pet_type
        self.cfg = Config()
        for key, value in kwargs.items():
            if hasattr(self.cfg, key): setattr(self.cfg, key, value)
        app_id, api_key, secret_key = self.cfg.BAIDU_KEYS
        self.speech_api = SpeechRecognition(app_id, api_key, secret_key)
        # 初始化
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint|Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.repaint()
        # 导入宠物
        if pet_type not in self.cfg.PET_ACTIONS_MAP: pet_type = None
        if pet_type is None:
            self.pet_images, iconpath = self.randomLoadPetImages()
        else:
            for name in list(self.cfg.PET_ACTIONS_MAP.keys()):
                if name != pet_type: self.cfg.PET_ACTIONS_MAP.pop(name)
            self.pet_images, iconpath = self.randomLoadPetImages()
        # 设置退出选项
        quit_action = QAction('退出', self, triggered=self.quit)
        quit_action.setIcon(QIcon(iconpath))
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(quit_action)
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(iconpath))
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        self.tray_icon.show()
        # 当前显示的图片
        self.image = QLabel(self)
        self.setImage(self.pet_images[0][0])
        # 是否跟随鼠标
        self.is_follow_mouse = False
        # 宠物拖拽时避免鼠标直接跳到左上角
        self.mouse_drag_pos = self.pos()
        # 显示
        self.resize(self.pet_images[0][0].size().width(), self.pet_images[0][0].size().height())
        self.randomPosition()
        self.show()
        # 宠物动画动作执行所需的一些变量
        self.is_running_action = False
        self.action_images = []
        self.action_pointer = 0
        self.action_max_len = 0
        # 每隔一段时间做个动作
        self.timer_act = QTimer()
        self.timer_act.timeout.connect(self.randomAct)
        self.timer_act.start(500)
        # 每隔一段时间检测一次语音
        self.timer_speech = QTimer()
        self.timer_speech.timeout.connect(self.talk)
        self.timer_speech.start(2000)
        self.running_talk = False
    '''对话功能实现'''
    def talk(self):
        if self.running_talk: return
        self.running_talk = True
        def _talk(self):
            valid_names = {'pikachu': '皮卡丘', 'blackcat': '黑猫', 'whitecat': '白猫', 'fox': '狐狸', 'bingdwendwen': '冰墩墩'}
            while True:
                self.speech_api.record()
                user_input = self.speech_api.recognition()
                if user_input is None: return
                if valid_names[self.pet_type] in user_input: break
                else: return
            self.speech_api.synthesisspeak('你好呀, 主人')
            while True:
                self.speech_api.record()
                user_input = self.speech_api.recognition()
                if user_input is None: continue
                if '再见' in user_input:
                    self.speech_api.synthesisspeak('好的, 主人再见')
                    self.running_talk = False
                    break
                else:
                    reply = self.turing(user_input)
                    self.speech_api.synthesisspeak(reply)
        threading.Thread(target=lambda: _talk(self)).start()
    '''图灵机器人API'''
    def turing(self, inputs):
        appkeys = [
            'f0a5ab746c7d41c48a733cabff23fb6d', 'c4fae3a2f8394b73bcffdecbbb4c6ac6', '0ca694db371745668c28c6cb0a755587',
            '7855ce1ebd654f31938505bb990616d4', '5945954988d24ed393f465aae9be71b9', '1a337b641da04c64aa7fd4849a5f713e',
            'eb720a8970964f3f855d863d24406576', '1107d5601866433dba9599fac1bc0083', '70a315f07d324b3ea02cf21d13796605',
            '45fa933f47bb45fb8e7746759ba9b24a', '2f1446eb0321804291b0a1e217c25bb5', '7f05e31d381143d9948109e75484d9d0',
            '35ff2856b55e4a7f9eeb86e3437e23fe', '820c4a6ca4694063ab6002be1d1c63d3',
        ]
        while True:
            url = 'http://www.tuling123.com/openapi/api?key=%s&info=%s'
            response = requests.get(url % (random.choice(appkeys), inputs))
            reply = response.json()['text']
            if u'当天请求次数已用完' in reply: continue
            return reply
    '''随机做一个动作'''
    def randomAct(self):
        if not self.is_running_action:
            self.is_running_action = True
            self.action_images = random.choice(self.pet_images)
            self.action_max_len = len(self.action_images)
            self.action_pointer = 0
        self.runFrame()
    '''完成动作的每一帧'''
    def runFrame(self):
        if self.action_pointer == self.action_max_len:
            self.is_running_action = False
            self.action_pointer = 0
            self.action_max_len = 0
        self.setImage(self.action_images[self.action_pointer])
        self.action_pointer += 1
    '''设置当前显示的图片'''
    def setImage(self, image):
        self.image.setPixmap(QPixmap.fromImage(image))
    '''随机导入一个桌面宠物的所有图片'''
    def randomLoadPetImages(self):
        cfg = self.cfg
        pet_name = random.choice(list(cfg.PET_ACTIONS_MAP.keys()))
        actions = cfg.PET_ACTIONS_MAP[pet_name]
        pet_images = []
        for action in actions:
            pet_images.append([self.loadImage(os.path.join(cfg.ROOT_DIR, pet_name, 'shime'+item+'.png')) for item in action])
        iconpath = os.path.join(cfg.ROOT_DIR, pet_name, 'shime1.png')
        return pet_images, iconpath
    '''鼠标左键按下时, 宠物将和鼠标位置绑定'''
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
    '''鼠标移动, 则宠物也移动'''
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            event.accept()
    '''鼠标释放时, 取消绑定'''
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))
    '''导入图像'''
    def loadImage(self, imagepath):
        image = QImage()
        image.load(imagepath)
        return image
    '''随机到一个屏幕上的某个位置'''
    def randomPosition(self):
        screen_geo = QDesktopWidget().screenGeometry()
        pet_geo = self.geometry()
        width = (screen_geo.width() - pet_geo.width()) * random.random()
        height = (screen_geo.height() - pet_geo.height()) * random.random()
        self.move(width, height)
    '''退出程序'''
    def quit(self):
        self.close()
        sys.exit()