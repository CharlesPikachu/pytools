'''
Function:
    简易端口扫描器
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import time
import socket
import threading


'''简单的端口扫描器'''
class PortScanner(threading.Thread):
    tool_name = '简易端口扫描器'
    def __init__(self, target_ip='127.0.0.1', port_min=0, port_max=65535, savedir='.', savename='result.txt', **kwargs):
        threading.Thread.__init__(self)
        assert isinstance(port_max, int) and isinstance(port_min, int)
        self.target_ip = target_ip
        self.port_min = max(0, port_min)
        self.port_max = min(65535, port_max)
        self.savepath = os.path.join(savedir, savename)
    '''运行'''
    def run(self):
        return self.__checker()
    '''检测'''
    def __checker(self):
        for port in range(self.port_min, self.port_max+1):
            self.__connect(port)
    '''连接'''
    def __connect(self, port):
        socket.setdefaulttimeout(1)
        s = socket.socket()
        try:
            t_start = time.time()
            s.connect((self.target_ip, port))
            t_end = time.time()
            flag = True
        except:
            flag = False
        s.close()
        if flag:
            connect_time = str(int((t_end - t_start) * 1000))
            info = 'Find --> [IP]: %s, [PORT]: %s, [Connect Time]: %s' % (self.target_ip, port, connect_time)
            print(info)
            self.__save(info)
        return flag
    '''保存结果'''
    def __save(self, content):
        if content:
            try:
                with open(self.savepath, 'a') as f:
                    f.write(content + '\n')
            except:
                time.sleep(0.1)