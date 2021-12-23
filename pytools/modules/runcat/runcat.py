'''
Function:
    奔跑的猫
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import sys
import time
import psutil
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon


'''奔跑的猫'''
class RunCat():
    tool_name = '奔跑的猫'
    def __init__(self, monitor_type='cpu', **kwargs):
        assert monitor_type in ['cpu', 'memory']
        self.rootdir = os.path.split(os.path.abspath(__file__))[0]
        self.monitor_type = monitor_type
    '''运行'''
    def run(self):
        if self.monitor_type == 'cpu':
            self.runcatCPU()
        elif self.monitor_type == 'memory':
            self.runcatMemory()
    '''奔跑的猫-CPU'''
    def runcatCPU(self):
        app = QApplication(sys.argv)
        # 最后一个可视的窗口退出时程序不退出
        app.setQuitOnLastWindowClosed(False)
        icon = QSystemTrayIcon()
        icon.setIcon(QIcon(os.path.join(self.rootdir, 'resources/0.png')))
        icon.setVisible(True)
        cpu_percent = psutil.cpu_percent(interval=1) / 100
        cpu_percent_update_fps = 20
        fps_count = 0
        while True:
            fps_count += 1
            if fps_count > cpu_percent_update_fps:
                cpu_percent = psutil.cpu_percent(interval=1) / 100
                fps_count = 0
            # 开口向上的抛物线, 左边递减
            time_interval = (cpu_percent * cpu_percent - 2 * cpu_percent + 2) / 20
            for i in range(5):
                icon.setIcon(QIcon(os.path.join(self.rootdir, 'resources/%d.png' % i)))
                icon.setToolTip('cpu: %.2f' % cpu_percent)
                time.sleep(time_interval)
        app.exec_()
    '''奔跑的猫-内存'''
    def runcatMemory(self):
        app = QApplication(sys.argv)
        # 最后一个可视的窗口退出时程序不退出
        app.setQuitOnLastWindowClosed(False)
        icon = QSystemTrayIcon()
        icon.setIcon(QIcon(os.path.join(self.rootdir, 'resources/0.png')))
        icon.setVisible(True)
        memory_percent = psutil.virtual_memory().percent / 100
        memory_percent_update_fps = 20
        fps_count = 0
        while True:
            fps_count += 1
            if fps_count > memory_percent_update_fps:
                memory_percent = psutil.virtual_memory().percent / 100
                fps_count = 0
            # 开口向上的抛物线, 左边递减
            time_interval = (memory_percent * memory_percent - 2 * memory_percent + 2) / 20
            for i in range(5):
                icon.setIcon(QIcon(os.path.join(self.rootdir, 'resources/%d.png' % i)))
                icon.setToolTip('memory: %.2f' % memory_percent)
                time.sleep(time_interval)
        app.exec_()