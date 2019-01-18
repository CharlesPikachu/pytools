'''
Function:
	tkinter计算器
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import math
import tkinter


root = tkinter.Tk()
root.resizable(width=False, height=False)
'''hypeparameter'''
# 是否按下了运算符
IS_CALC = False
# 存储数字
STORAGE = []
# 显示框最多显示多少个字符
MAXSHOWLEN = 18
# 当前显示的数字
CurrentShow = tkinter.StringVar()
CurrentShow.set('0')


'''按下数字键(0-9)'''
def pressNumber(number):
	global IS_CALC
	if IS_CALC:
		CurrentShow.set('0')
		IS_CALC = False
	if CurrentShow.get() == '0':
		CurrentShow.set(number)
	else:
		if len(CurrentShow.get()) < MAXSHOWLEN:
			CurrentShow.set(CurrentShow.get() + number)


'''按下小数点'''
def pressDP():
	global IS_CALC
	if IS_CALC:
		CurrentShow.set('0')
		IS_CALC = False
	if len(CurrentShow.get().split('.')) == 1:
		if len(CurrentShow.get()) < MAXSHOWLEN:
			CurrentShow.set(CurrentShow.get() + '.')


'''清零'''
def clearAll():
	global STORAGE
	global IS_CALC
	STORAGE.clear()
	IS_CALC = False
	CurrentShow.set('0')


'''清除当前显示框内所有数字'''
def clearCurrent():
	CurrentShow.set('0')


'''删除显示框内最后一个数字'''
def delOne():
	global IS_CALC
	if IS_CALC:
		CurrentShow.set('0')
		IS_CALC = False
	if CurrentShow.get() != '0':
		if len(CurrentShow.get()) > 1:
			CurrentShow.set(CurrentShow.get()[:-1])
		else:
			CurrentShow.set('0')


'''计算答案修正'''
def modifyResult(result):
	result = str(result)
	if len(result) > MAXSHOWLEN:
		if len(result.split('.')[0]) > MAXSHOWLEN:
			result = 'Overflow'
		else:
			# 直接舍去不考虑四舍五入问题
			result = result[:MAXSHOWLEN]
	return result


'''按下运算符'''
def pressOperator(operator):
	global STORAGE
	global IS_CALC
	if operator == '+/-':
		if CurrentShow.get().startswith('-'):
			CurrentShow.set(CurrentShow.get()[1:])
		else:
			CurrentShow.set('-'+CurrentShow.get())
	elif operator == '1/x':
		try:
			result = 1 / float(CurrentShow.get())
		except:
			result = 'illegal operation'
		result = modifyResult(result)
		CurrentShow.set(result)
		IS_CALC = True
	elif operator == 'sqrt':
		try:
			result = math.sqrt(float(CurrentShow.get()))
		except:
			result = 'illegal operation'
		result = modifyResult(result)
		CurrentShow.set(result)
		IS_CALC = True
	elif operator == 'MC':
		STORAGE.clear()
	elif operator == 'MR':
		if IS_CALC:
			CurrentShow.set('0')
		STORAGE.append(CurrentShow.get())
		expression = ''.join(STORAGE)
		try:
			result = eval(expression)
		except:
			result = 'illegal operation'
		result = modifyResult(result)
		CurrentShow.set(result)
		IS_CALC = True
	elif operator == 'MS':
		STORAGE.clear()
		STORAGE.append(CurrentShow.get())
	elif operator == 'M+':
		STORAGE.append(CurrentShow.get())
	elif operator == 'M-':
		if CurrentShow.get().startswith('-'):
			STORAGE.append(CurrentShow.get())
		else:
			STORAGE.append('-' + CurrentShow.get())
	elif operator in ['+', '-', '*', '/', '%']:
		STORAGE.append(CurrentShow.get())
		STORAGE.append(operator)
		IS_CALC = True
	elif operator == '=':
		if IS_CALC:
			CurrentShow.set('0')
		STORAGE.append(CurrentShow.get())
		expression = ''.join(STORAGE)
		try:
			result = eval(expression)
		# 除以0的情况
		except:
			result = 'illegal operation'
		result = modifyResult(result)
		CurrentShow.set(result)
		STORAGE.clear()
		IS_CALC = True


'''Demo'''
def Demo():
	root.minsize(320, 420)
	root.title('Calculator')
	# 布局
	# --文本框
	label = tkinter.Label(root, textvariable=CurrentShow, bg='black', anchor='e', bd=5, fg='white', font=('楷体', 20))
	label.place(x=20, y=50, width=280, height=50)
	# --第一行
	# ----Memory clear
	button1_1 = tkinter.Button(text='MC', bg='#666', bd=2, command=lambda:pressOperator('MC'))
	button1_1.place(x=20, y=110, width=50, height=35)
	# ----Memory read
	button1_2 = tkinter.Button(text='MR', bg='#666', bd=2, command=lambda:pressOperator('MR'))
	button1_2.place(x=77.5, y=110, width=50, height=35)
	# ----Memory save
	button1_3 = tkinter.Button(text='MS', bg='#666', bd=2, command=lambda:pressOperator('MS'))
	button1_3.place(x=135, y=110, width=50, height=35)
	# ----Memory +
	button1_4 = tkinter.Button(text='M+', bg='#666', bd=2, command=lambda:pressOperator('M+'))
	button1_4.place(x=192.5, y=110, width=50, height=35)
	# ----Memory -
	button1_5 = tkinter.Button(text='M-', bg='#666', bd=2, command=lambda:pressOperator('M-'))
	button1_5.place(x=250, y=110, width=50, height=35)
	# --第二行
	# ----删除单个数字
	button2_1 = tkinter.Button(text='del', bg='#666', bd=2, command=lambda:delOne())
	button2_1.place(x=20, y=155, width=50, height=35)
	# ----清除当前显示框内所有数字
	button2_2 = tkinter.Button(text='CE', bg='#666', bd=2, command=lambda:clearCurrent())
	button2_2.place(x=77.5, y=155, width=50, height=35)
	# ----清零(相当于重启)
	button2_3 = tkinter.Button(text='C', bg='#666', bd=2, command=lambda:clearAll())
	button2_3.place(x=135, y=155, width=50, height=35)
	# ----取反
	button2_4 = tkinter.Button(text='+/-', bg='#666', bd=2, command=lambda:pressOperator('+/-'))
	button2_4.place(x=192.5, y=155, width=50, height=35)
	# ----开根号
	button2_5 = tkinter.Button(text='sqrt', bg='#666', bd=2, command=lambda:pressOperator('sqrt'))
	button2_5.place(x=250, y=155, width=50, height=35)
	# --第三行
	# ----7
	button3_1 = tkinter.Button(text='7', bg='#bbbbbb', bd=2, command=lambda:pressNumber('7'))
	button3_1.place(x=20, y=200, width=50, height=35)
	# ----8
	button3_2 = tkinter.Button(text='8', bg='#bbbbbb', bd=2, command=lambda:pressNumber('8'))
	button3_2.place(x=77.5, y=200, width=50, height=35)
	# ----9
	button3_3 = tkinter.Button(text='9', bg='#bbbbbb', bd=2, command=lambda:pressNumber('9'))
	button3_3.place(x=135, y=200, width=50, height=35)
	# ----除
	button3_4 = tkinter.Button(text='/', bg='#708069', bd=2, command=lambda:pressOperator('/'))
	button3_4.place(x=192.5, y=200, width=50, height=35)
	# ----取余
	button3_5 = tkinter.Button(text='%', bg='#708069', bd=2, command=lambda:pressOperator('%'))
	button3_5.place(x=250, y=200, width=50, height=35)
	# --第四行
	# ----4
	button4_1 = tkinter.Button(text='4', bg='#bbbbbb', bd=2, command=lambda:pressNumber('4'))
	button4_1.place(x=20, y=245, width=50, height=35)
	# ----5
	button4_2 = tkinter.Button(text='5', bg='#bbbbbb', bd=2, command=lambda:pressNumber('5'))
	button4_2.place(x=77.5, y=245, width=50, height=35)
	# ----6
	button4_3 = tkinter.Button(text='6', bg='#bbbbbb', bd=2, command=lambda:pressNumber('6'))
	button4_3.place(x=135, y=245, width=50, height=35)
	# ----乘
	button4_4 = tkinter.Button(text='*', bg='#708069', bd=2, command=lambda:pressOperator('*'))
	button4_4.place(x=192.5, y=245, width=50, height=35)
	# ----取导数
	button4_5 = tkinter.Button(text='1/x', bg='#708069', bd=2, command=lambda:pressOperator('1/x'))
	button4_5.place(x=250, y=245, width=50, height=35)
	# --第五行
	# ----3
	button5_1 = tkinter.Button(text='3', bg='#bbbbbb', bd=2, command=lambda:pressNumber('3'))
	button5_1.place(x=20, y=290, width=50, height=35)
	# ----2
	button5_2 = tkinter.Button(text='2', bg='#bbbbbb', bd=2, command=lambda:pressNumber('2'))
	button5_2.place(x=77.5, y=290, width=50, height=35)
	# ----1
	button5_3 = tkinter.Button(text='1', bg='#bbbbbb', bd=2, command=lambda:pressNumber('1'))
	button5_3.place(x=135, y=290, width=50, height=35)
	# ----减
	button5_4 = tkinter.Button(text='-', bg='#708069', bd=2, command=lambda:pressOperator('-'))
	button5_4.place(x=192.5, y=290, width=50, height=35)
	# ----等于
	button5_5 = tkinter.Button(text='=', bg='#708069', bd=2, command=lambda:pressOperator('='))
	button5_5.place(x=250, y=290, width=50, height=80)
	# --第六行
	# ----0
	button6_1 = tkinter.Button(text='0', bg='#bbbbbb', bd=2, command=lambda:pressNumber('0'))
	button6_1.place(x=20, y=335, width=107.5, height=35)
	# ----小数点
	button6_2 = tkinter.Button(text='.', bg='#bbbbbb', bd=2, command=lambda:pressDP())
	button6_2.place(x=135, y=335, width=50, height=35)
	# ----加
	button6_3 = tkinter.Button(text='+', bg='#708069', bd=2, command=lambda:pressOperator('+'))
	button6_3.place(x=192.5, y=335, width=50, height=35)
	root.mainloop()


if __name__ == '__main__':
	Demo()