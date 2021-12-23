'''
Function:
    仿抖音表白神器
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import sys
import random
import pygame
from tkinter import Tk, messagebox


'''配置信息'''
class Config():
    rootdir = os.path.split(os.path.abspath(__file__))[0]
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
    BGM_PATH = os.path.join(rootdir, 'resources/music/bgm.mp3')
    # 字体路径
    FONT_PATH = os.path.join(rootdir, 'resources/font/STXINGKA.TTF')
    # 背景图片路径
    BG_IMAGE_PATH = os.path.join(rootdir, 'resources/images/bg.png')
    # ICON路径
    ICON_IMAGE_PATH = os.path.join(rootdir, 'resources/images/icon.png')


'''按钮类'''
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, fontpath, fontsize, fontcolor, bgcolors, edgecolor, edgesize=1, is_want_to_be_selected=True, screensize=None, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(fontpath, fontsize)
        self.fontcolor = fontcolor
        self.bgcolors = bgcolors
        self.edgecolor = edgecolor
        self.edgesize = edgesize
        self.is_want_tobe_selected = is_want_to_be_selected
        self.screensize = screensize
    '''自动根据各种情况将按钮绑定到屏幕'''
    def draw(self, screen, mouse_pos):
        # 鼠标在按钮范围内
        if self.rect.collidepoint(mouse_pos):
            # --不想被选中
            if not self.is_want_tobe_selected:
                while self.rect.collidepoint(mouse_pos):
                    self.rect.left, self.rect.top = random.randint(0, self.screensize[0]-self.rect.width), random.randint(0, self.screensize[1]-self.rect.height)
            pygame.draw.rect(screen, self.bgcolors[0], self.rect, 0)
            pygame.draw.rect(screen, self.edgecolor, self.rect, self.edgesize)
        # 鼠标不在按钮范围内
        else:
            pygame.draw.rect(screen, self.bgcolors[1], self.rect, 0)
            pygame.draw.rect(screen, self.edgecolor, self.rect, self.edgesize)
        text_render = self.font.render(self.text, True, self.fontcolor)
        fontsize = self.font.size(self.text)
        screen.blit(text_render, (self.rect.x+(self.rect.width-fontsize[0])/2, self.rect.y+(self.rect.height-fontsize[1])/2))


'''在指定位置显示文字'''
def showText(screen, text, position, fontpath, fontsize, fontcolor, is_bold=False):
    font = pygame.font.Font(fontpath, fontsize)
    font.set_bold(is_bold)
    text_render = font.render(text, True, fontcolor)
    screen.blit(text_render, position)


'''仿抖音表白神器'''
class NaughtyConfession():
    tool_name = '仿抖音表白神器'
    def __init__(self, title='来自一位喜欢你的小哥哥', **kwargs):
        self.title = title
        self.cfg = Config()
        for key, value in kwargs.items():
            if hasattr(self.cfg, key): setattr(self.cfg, key, value)
    def run(self):
        cfg = self.cfg
        # 初始化
        pygame.init()
        screen = pygame.display.set_mode(cfg.SCREENSIZE, 0, 32)
        pygame.display.set_icon(pygame.image.load(cfg.ICON_IMAGE_PATH))
        pygame.display.set_caption(self.title)
        # 背景音乐
        pygame.mixer.music.load(cfg.BGM_PATH)
        pygame.mixer.music.play(-1, 30.0)
        # biu爱心那个背景图片
        bg_image = pygame.image.load(cfg.BG_IMAGE_PATH)
        bg_image = pygame.transform.smoothscale(bg_image, (150, 150))
        # 实例化两个按钮
        button_yes = Button(
            x=20, y=cfg.SCREENSIZE[1]-70, width=120, height=35, 
            text='好呀', fontpath=cfg.FONT_PATH, fontsize=15, fontcolor=cfg.BLACK, edgecolor=cfg.SKYBLUE, 
            edgesize=2, bgcolors=[cfg.DARKGRAY, cfg.GAINSBORO], is_want_to_be_selected=True, screensize=cfg.SCREENSIZE
        )
        button_no = Button(
            x=cfg.SCREENSIZE[0]-140, y=cfg.SCREENSIZE[1]-70, width=120, height=35, 
            text='算了吧', fontpath=cfg.FONT_PATH, fontsize=15, fontcolor=cfg.BLACK, edgecolor=cfg.DARKGRAY, 
            edgesize=1, bgcolors=[cfg.DARKGRAY, cfg.GAINSBORO], is_want_to_be_selected=False, screensize=cfg.SCREENSIZE
        )
        # 是否点击了好呀按钮
        is_agree = False
        # 主循环
        clock = pygame.time.Clock()
        while True:
            # --背景图片
            screen.fill(cfg.WHITE)
            screen.blit(bg_image, (cfg.SCREENSIZE[0]-bg_image.get_height(), 0))
            # --鼠标事件捕获
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # ----没有点击好呀按钮之前不许退出程序
                    if is_agree:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
                    if button_yes.rect.collidepoint(pygame.mouse.get_pos()):
                        button_yes.is_selected = True
                        root = Tk()
                        root.withdraw()
                        messagebox.showinfo('', '❤❤❤么么哒❤❤❤')
                        root.destroy()
                        is_agree = True
            # --显示文字
            showText(screen=screen, text='小姐姐, 我观察你很久了', position=(40, 50), fontpath=cfg.FONT_PATH, fontsize=25, fontcolor=cfg.BLACK, is_bold=False)
            showText(screen=screen, text='做我女朋友好不好?', position=(40, 100), fontpath=cfg.FONT_PATH, fontsize=25, fontcolor=cfg.BLACK, is_bold=True)
            # --显示按钮
            button_yes.draw(screen, pygame.mouse.get_pos())
            button_no.draw(screen, pygame.mouse.get_pos())
            # --刷新
            pygame.display.update()
            clock.tick(60)