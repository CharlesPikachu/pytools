'''
Function:
	简单计时器
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui


'''
Function:
	将时间转为<A:BC.D>格式
'''
def Convert(t):
	D = t % 10
	# 十位
	B = (t // 100) % 6
	# 个位
	C = (t // 10) % 10
	# 分钟
	A = t // 600
	return str(A) + ':' + str(B) + str(C) + '.' + str(D)


'''
Function:
	开始计时
'''
def Start():
	global timer, color
	color = 'white'
	if not timer.is_running():
		timer.start()


'''
Function:
	停止计时
'''
def Stop():
	global timer, color
	timer.stop()
	color = 'red'


'''
Function:
	清空
'''
def Clear():
	global t, timer, color
	timer.stop()
	t = 0
	color = 'white'


'''
Function:
	计时器
'''
def timerHandler():
	global t
	t += 1


'''
Function:
	绘制时间
'''
def drawHandler(canvas):
	t_convert = Convert(t)
	canvas.draw_text(t_convert, (25, 120), 60, color, 'serif')


'''
Function:
	主函数
'''
def main():
	global t, color
	t = 0
	color = 'white'
	frame = simplegui.create_frame('Timer', 200, 200, 150)
	# 1000 / 100 = 10, 即t自加10次为一秒
	global timer
	timer = simplegui.create_timer(100, timerHandler)
	frame.set_draw_handler(drawHandler)
	button_start = frame.add_button('Start', Start, 150)
	button_stop = frame.add_button('Stop', Stop, 150)
	button_clear = frame.add_button('Clear', Clear, 150)
	frame.start()


if __name__ == '__main__':
	main()