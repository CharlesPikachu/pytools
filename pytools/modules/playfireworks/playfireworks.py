'''
Function:
    放烟花效果
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import sys
import math
import time
import pygame
import random


'''配置信息'''
class Config:
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # 屏幕大小
    SCREENSIZE = (1152, 720)
    # 标题
    TITLE = '新年烟花 —— Charles的皮卡丘'
    # FPS
    FPS = 60
    # 背景图片
    IMAGEPATH = os.path.join(rootdir, 'resources/bg.jpg')
    USE_IMAGEPATH = False if random.random() > 0.5 else True
    # 背景音乐
    BGMPATH = os.path.join(rootdir, 'resources/bgm.mp3')
    # ICON
    ICONPATH = os.path.join(rootdir, 'resources/icon.ico')


'''工具函数'''
class Utils():
    '''随机速度'''
    @staticmethod
    def randv():
        return random.uniform(15, 22)
    '''随机颜色'''
    @staticmethod
    def randc():
        colors_list = [
            (244, 214, 215), (55, 20, 88), (151, 68, 114), (230, 190, 146), (244, 252, 255), (230, 197, 246), 
            (181, 180, 222), (191, 85, 177), (255, 199, 209), (200, 50, 66), (223, 219, 216), (158, 167, 164), 
            (173, 254, 255), (185, 219, 149), (72, 141, 235), (252, 117, 249), (232, 169, 180), (155, 157, 170), 
            (182, 98, 130), (248, 215, 20), (136, 214, 253), (221, 0, 27)
        ]
        return colors_list[random.randint(0, len(colors_list) - 1)]


'''烟花颗粒'''
class Point(pygame.sprite.Sprite):
    def __init__(self, speed=None, position=None, color=None):
        pygame.sprite.Sprite.__init__(self)
        # 图片
        self.image = pygame.Surface((15, 15))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.color = Utils().randc() if color is None else color
        pygame.draw.circle(self.image, self.color, (8, 8), random.uniform(3, 4))
        self.rect = self.image.get_rect()
        # 初始位置
        self.rect.center = position
        # 速度 (x方向, y方向)
        self.speed = list(speed)
        # 存在的时间
        self.count = 0
        self.max_counts = 55
        self.is_explode = False
    '''更新'''
    def update(self, radius):
        self.move()
        if self.rect.y > Config.SCREENSIZE[1] - 20 and self.is_explode:
            self.kill()
        if self.speed[1] < 1 and not self.is_explode:
            self.explode(radius)
        if self.is_explode:
            self.count += 1
            if self.count > self.max_counts:
                self.kill()
    '''移动'''
    def move(self):
        t, g = 1 / 60, 9.8
        self.rect.x += self.speed[0] * t * 25
        self.rect.y -= (2 * self.speed[1] - g * t) * t / 2 * 25
        self.speed[1] = self.speed[1] - g * t
    '''爆炸'''
    def explode(self, radius):
        self.is_explode = True
        angle = random.randint(0, 359) * math.pi / 180
        self.speed[0] += math.cos(angle) * radius
        self.speed[1] -= math.sin(angle) * radius


'''定义烟花'''
class Fireworks(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.points = pygame.sprite.Group()
        self.speed = (0, Utils().randv())
        self.position = (Config.SCREENSIZE[0] * random.random(), Config.SCREENSIZE[1] - 10)
        color = Utils().randc()
        for _ in range(random.randint(30, 40)):
            self.points.add(Point(
                speed=self.speed, 
                position=self.position, 
                color=None if random.random() > 0.5 else color
            ))
        self.start_time = time.time()
    '''画到屏幕上'''
    def draw(self, screen):
        self.points.draw(screen)
    '''更新'''
    def update(self):
        radius = random.uniform(8, 10)
        self.points.update(radius)
        if (time.time() - self.start_time > 5): return True
        else: return False


'''放烟花效果'''
class PlayFireworks():
    tool_name = '放烟花效果'
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
    '''运行'''
    def run(self):
        # 初始化
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode(Config.SCREENSIZE)
        pygame.display.set_caption(Config.TITLE)
        pygame.display.set_icon(pygame.image.load(Config.ICONPATH).convert())
        # 背景音乐
        bgm = pygame.mixer.music.load(Config.BGMPATH)
        pygame.mixer.music.play(-1)
        # 定义烟花
        fireworks_list = pygame.sprite.Group()
        for _ in range(15): fireworks_list.add(Fireworks())
        # 主循环
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            screen.fill((0, 0, 0))
            if Config().USE_IMAGEPATH:
                screen.blit(pygame.transform.scale(pygame.image.load(Config.IMAGEPATH), Config.SCREENSIZE), (0, 0))
            if random.random() < 8 / 60: fireworks_list.add(Fireworks())
            for item in fireworks_list:
                if item.update():
                    fireworks_list.remove(item)
                item.draw(screen)
            pygame.display.flip()
            clock.tick(Config.FPS)