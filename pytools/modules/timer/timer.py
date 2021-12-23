'''
Function:
    简易计时器
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


'''简易计时器'''
class Timer():
    tool_name = '简易计时器'
    def __init__(self, start_color='white', stop_color='red', title='简易计时器 —— Charles的皮卡丘', **kwargs):
        self.title = title
        self.color = start_color
        self.start_color = start_color
        self.stop_color = stop_color
        self.time_count = 0
    '''将时间转为<A:BC.D>格式'''
    def convert(self, time_count):
        D = time_count % 10
        # 十位
        B = (time_count // 100) % 6
        # 个位
        C = (time_count // 10) % 10
        # 分钟
        A = time_count // 600
        return str(A) + ':' + str(B) + str(C) + '.' + str(D)
    '''开始计时'''
    def start(self):
        self.color = self.start_color
        if not self.timer.is_running(): self.timer.start()
    '''计时器'''
    def timerhandler(self):
        self.time_count += 1
    '''停止计时'''
    def stop(self):
        self.color = self.stop_color
        self.timer.stop()
    '''清空'''
    def clear(self):
        self.timer.stop()
        self.color = self.start_color
        self.time_count = 0
    '''绘制时间'''
    def drawhandler(self, canvas):
        t_convert = self.convert(self.time_count)
        canvas.draw_text(t_convert, (25, 120), 60, self.color, 'serif')
    '''运行'''
    def run(self):
        frame = simplegui.create_frame(self.title, 200, 200, 150)
        self.timer = simplegui.create_timer(100, self.timerhandler)
        frame.set_draw_handler(self.drawhandler)
        button_start = frame.add_button('Start', self.start, 150)
        button_stop = frame.add_button('Stop', self.stop, 150)
        button_clear = frame.add_button('Clear', self.clear, 150)
        frame.start()