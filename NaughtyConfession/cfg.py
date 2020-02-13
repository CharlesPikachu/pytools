'''配置文件'''
import os


# 窗口大小(width, height)
SCREENSIZE = (500, 260)
# 定义一些颜色
RED = (255, 0, 0)
BLACK = (0, 0, 0)
AZURE = (240, 255, 255)
WHITE = (255, 255, 255)
MISTYROSE = (255, 228, 225)
PALETURQUOISE = (175, 238, 238)
PAPAYAWHIP = (255, 239, 213)
LIGHTGRAY = (211, 211, 211)
GAINSBORO = (230, 230, 230)
WHITESMOKE = (245, 245, 245)
DARKGRAY = (169, 169, 169)
BLUE = (0, 0, 255)
DEEPSKYBLUE = (0, 191, 255)
SKYBLUE = (135, 206, 235)
LIGHTSKYBLUE = (135, 206, 250)
# 背景音乐路径
BGM_PATH = os.path.join(os.getcwd(), 'resources/music/bgm.mp3')
# 字体路径
FONT_PATH = os.path.join(os.getcwd(), 'resources/font/STXINGKA.TTF')
# 背景图片路径
BG_IMAGE_PATH = os.path.join(os.getcwd(), 'resources/images/bg.png')
# ICON路径
ICON_IMAGE_PATH = os.path.join(os.getcwd(), 'resources/images/icon.png')