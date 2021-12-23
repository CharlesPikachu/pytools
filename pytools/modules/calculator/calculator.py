'''
Function:
    简易计算器
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import math
import tkinter


'''简易计算器'''
class Calculator():
    tool_name = '简易计算器'
    def __init__(self, title='简易计算器 —— Charles的皮卡丘', root_size=(320, 420), **kwargs):
        # 基本界面
        self.root = tkinter.Tk()
        self.root.resizable(width=False, height=False)
        self.root.minsize(*root_size)
        self.root.title(title)
        # 参数初始化
        self.storage = []
        self.is_calculate = False
        self.max_show_len = kwargs.get('max_show_len', 18)
        self.current_show = tkinter.StringVar()
        self.current_show.set('0')
    '''全部清零'''
    def reset(self):
        self.storage.clear()
        self.is_calculate = False
        self.current_show.set('0')
    '''清除当前显示框内所有数字'''
    def clearcurrentshow(self):
        self.current_show.set('0')
    '''按下数字键(0-9)'''
    def pressnumber(self, number):
        if self.is_calculate:
            self.current_show.set('0')
            self.is_calculate = False
        if self.current_show.get() == '0':
            self.current_show.set(number)
        else:
            if len(self.current_show.get()) < self.max_show_len: self.current_show.set(self.current_show.get() + number)
    '''按下小数点'''
    def pressdp(self):
        if self.is_calculate:
            self.current_show.set('0')
            self.is_calculate = False
        if len(self.current_show.get().split('.')) == 1:
            if len(self.current_show.get()) < self.max_show_len: self.current_show.set(self.current_show.get() + '.')
    '''删除显示框内最后一个数字'''
    def delete(self):
        if self.is_calculate:
            self.current_show.set('0')
            self.is_calculate = False
        if self.current_show.get() != '0':
            if len(self.current_show.get()) > 1: self.current_show.set(self.current_show.get()[:-1])
            else: self.current_show.set('0')
    '''计算答案修正'''
    def modify(self, result):
        result = str(result)
        if len(result) > self.max_show_len:
            if len(result.split('.')[0]) > self.max_show_len: result = 'Overflow'
            else: result = result[:self.max_show_len]
        return result
    '''按下运算符'''
    def pressoperator(self, operator):
        # 取反
        if operator == '+/-':
            if self.current_show.get().startswith('-'): self.current_show.set(self.current_show.get()[1:])
            else: self.current_show.set('-'+self.current_show.get())
        # 取倒数
        elif operator == '1/x':
            try: result = 1 / float(self.current_show.get())
            except: result = 'illegal operation'
            result = self.modify(result)
            self.current_show.set(result)
            self.is_calculate = True
        # 求平方根
        elif operator == 'sqrt':
            try: result = math.sqrt(float(self.current_show.get()))
            except: result = 'illegal operation'
            result = self.modify(result)
            self.current_show.set(result)
            self.is_calculate = True
        # 清除storage
        elif operator == 'MC':
            self.storage.clear()
        # 把当前计算出来扽数字呈现出来
        elif operator == 'MR':
            if self.is_calculate: self.current_show.set('0')
            self.storage.append(self.current_show.get())
            expression = ''.join(self.storage)
            try: result = eval(expression)
            except: result = 'illegal operation'
            result = self.modify(result)
            self.current_show.set(result)
            self.is_calculate = True
        # 无视目前记忆多少数字, 直接以当前数字取代记忆中的数字
        elif operator == 'MS':
            self.storage.clear()
            self.storage.append(self.current_show.get())
        # 记忆当前数字, 加入累加数字当中
        elif operator == 'M+':
            self.storage.append(self.current_show.get())
        # 记忆当前数字, 以负数形式加入累加数字当中
        elif operator == 'M-':
            if self.current_show.get().startswith('-'): self.storage.append(self.current_show.get())
            else: self.storage.append('-' + self.current_show.get())
        # 加减乘除取余
        elif operator in ['+', '-', '*', '/', '%']:
            self.storage.append(self.current_show.get())
            self.storage.append(operator)
            self.is_calculate = True
        # 计算
        elif operator == '=':
            if self.is_calculate: self.current_show.set('0')
            self.storage.append(self.current_show.get())
            expression = ''.join(self.storage)
            try: result = eval(expression)
            except: result = 'illegal operation'
            result = self.modify(result)
            self.current_show.set(result)
            self.storage.clear()
            self.is_calculate = True
    '''运行'''
    def run(self):
        # 布局
        # --文本框
        label = tkinter.Label(self.root, textvariable=self.current_show, bg='black', anchor='e', bd=5, fg='white', font=('楷体', 20))
        label.place(x=20, y=50, width=280, height=50)
        # --第一行
        # ----Memory clear
        button1_1 = tkinter.Button(text='MC', bg='#666', bd=2, command=lambda: self.pressoperator('MC'))
        button1_1.place(x=20, y=110, width=50, height=35)
        # ----Memory read
        button1_2 = tkinter.Button(text='MR', bg='#666', bd=2, command=lambda: self.pressoperator('MR'))
        button1_2.place(x=77.5, y=110, width=50, height=35)
        # ----Memory save
        button1_3 = tkinter.Button(text='MS', bg='#666', bd=2, command=lambda: self.pressoperator('MS'))
        button1_3.place(x=135, y=110, width=50, height=35)
        # ----Memory +
        button1_4 = tkinter.Button(text='M+', bg='#666', bd=2, command=lambda: self.pressoperator('M+'))
        button1_4.place(x=192.5, y=110, width=50, height=35)
        # ----Memory -
        button1_5 = tkinter.Button(text='M-', bg='#666', bd=2, command=lambda: self.pressoperator('M-'))
        button1_5.place(x=250, y=110, width=50, height=35)
        # --第二行
        # ----删除单个数字
        button2_1 = tkinter.Button(text='del', bg='#666', bd=2, command=lambda: self.delete())
        button2_1.place(x=20, y=155, width=50, height=35)
        # ----清除当前显示框内所有数字
        button2_2 = tkinter.Button(text='CE', bg='#666', bd=2, command=lambda: self.clearcurrentshow())
        button2_2.place(x=77.5, y=155, width=50, height=35)
        # ----清零(相当于重启)
        button2_3 = tkinter.Button(text='C', bg='#666', bd=2, command=lambda: self.reset())
        button2_3.place(x=135, y=155, width=50, height=35)
        # ----取反
        button2_4 = tkinter.Button(text='+/-', bg='#666', bd=2, command=lambda: self.pressoperator('+/-'))
        button2_4.place(x=192.5, y=155, width=50, height=35)
        # ----开根号
        button2_5 = tkinter.Button(text='sqrt', bg='#666', bd=2, command=lambda: self.pressoperator('sqrt'))
        button2_5.place(x=250, y=155, width=50, height=35)
        # --第三行
        # ----7
        button3_1 = tkinter.Button(text='7', bg='#bbbbbb', bd=2, command=lambda: self.pressnumber('7'))
        button3_1.place(x=20, y=200, width=50, height=35)
        # ----8
        button3_2 = tkinter.Button(text='8', bg='#bbbbbb', bd=2, command=lambda: self.pressnumber('8'))
        button3_2.place(x=77.5, y=200, width=50, height=35)
        # ----9
        button3_3 = tkinter.Button(text='9', bg='#bbbbbb', bd=2, command=lambda: self.pressnumber('9'))
        button3_3.place(x=135, y=200, width=50, height=35)
        # ----除
        button3_4 = tkinter.Button(text='/', bg='#708069', bd=2, command=lambda: self.pressoperator('/'))
        button3_4.place(x=192.5, y=200, width=50, height=35)
        # ----取余
        button3_5 = tkinter.Button(text='%', bg='#708069', bd=2, command=lambda: self.pressoperator('%'))
        button3_5.place(x=250, y=200, width=50, height=35)
        # --第四行
        # ----4
        button4_1 = tkinter.Button(text='4', bg='#bbbbbb', bd=2, command=lambda: self.pressnumber('4'))
        button4_1.place(x=20, y=245, width=50, height=35)
        # ----5
        button4_2 = tkinter.Button(text='5', bg='#bbbbbb', bd=2, command=lambda: self.pressnumber('5'))
        button4_2.place(x=77.5, y=245, width=50, height=35)
        # ----6
        button4_3 = tkinter.Button(text='6', bg='#bbbbbb', bd=2, command=lambda: self.pressnumber('6'))
        button4_3.place(x=135, y=245, width=50, height=35)
        # ----乘
        button4_4 = tkinter.Button(text='*', bg='#708069', bd=2, command=lambda: self.pressoperator('*'))
        button4_4.place(x=192.5, y=245, width=50, height=35)
        # ----取导数
        button4_5 = tkinter.Button(text='1/x', bg='#708069', bd=2, command=lambda: self.pressoperator('1/x'))
        button4_5.place(x=250, y=245, width=50, height=35)
        # --第五行
        # ----3
        button5_1 = tkinter.Button(text='3', bg='#bbbbbb', bd=2, command=lambda: self.pressnumber('3'))
        button5_1.place(x=20, y=290, width=50, height=35)
        # ----2
        button5_2 = tkinter.Button(text='2', bg='#bbbbbb', bd=2, command=lambda: self.pressnumber('2'))
        button5_2.place(x=77.5, y=290, width=50, height=35)
        # ----1
        button5_3 = tkinter.Button(text='1', bg='#bbbbbb', bd=2, command=lambda: self.pressnumber('1'))
        button5_3.place(x=135, y=290, width=50, height=35)
        # ----减
        button5_4 = tkinter.Button(text='-', bg='#708069', bd=2, command=lambda: self.pressoperator('-'))
        button5_4.place(x=192.5, y=290, width=50, height=35)
        # ----等于
        button5_5 = tkinter.Button(text='=', bg='#708069', bd=2, command=lambda: self.pressoperator('='))
        button5_5.place(x=250, y=290, width=50, height=80)
        # --第六行
        # ----0
        button6_1 = tkinter.Button(text='0', bg='#bbbbbb', bd=2, command=lambda: self.pressnumber('0'))
        button6_1.place(x=20, y=335, width=107.5, height=35)
        # ----小数点
        button6_2 = tkinter.Button(text='.', bg='#bbbbbb', bd=2, command=lambda: self.pressdp())
        button6_2.place(x=135, y=335, width=50, height=35)
        # ----加
        button6_3 = tkinter.Button(text='+', bg='#708069', bd=2, command=lambda: self.pressoperator('+'))
        button6_3.place(x=192.5, y=335, width=50, height=35)
        # 运行
        self.root.mainloop()