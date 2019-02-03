'''
Function:
	Python制作简易时钟
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import turtle
import datetime


'''悬空移动'''
def move(distance):
	turtle.penup()
	turtle.forward(distance)
	turtle.pendown()


'''创建表针turtle'''
def createHand(name, length):
	turtle.reset()
	move(-length * 0.01)
	turtle.begin_poly()
	turtle.forward(length * 1.01)
	turtle.end_poly()
	hand = turtle.get_poly()
	turtle.register_shape(name, hand)


'''创建时钟'''
def createClock(radius):
	turtle.reset()
	turtle.pensize(7)
	for i in range(60):
		move(radius)
		if i % 5 == 0:
			turtle.forward(20)
			move(-radius-20)
		else:
			turtle.dot(5)
			move(-radius)
		turtle.right(6)


'''获得今天是星期几'''
def getWeekday(today):
	return ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'][today.weekday()]


'''获得今天的日期'''
def getDate(today):
	return '%s年%s月%s日' % (today.year, today.month, today.day)


'''动态显示表针'''
def startTick(second_hand, minute_hand, hour_hand, printer):
	today = datetime.datetime.today()
	second = today.second + today.microsecond * 1e-6
	minute = today.minute + second / 60.
	hour = (today.hour + minute / 60) % 12
	# 设置朝向
	second_hand.setheading(6 * second)
	minute_hand.setheading(6 * minute)
	hour_hand.setheading(12 * hour)
	turtle.tracer(False)
	printer.forward(65)
	printer.write(getWeekday(today), align='center', font=("Courier", 14, "bold"))
	printer.forward(120)
	printer.write('12', align='center', font=("Courier", 14, "bold"))
	printer.back(250)
	printer.write(getDate(today), align='center', font=("Courier", 14, "bold"))
	printer.back(145)
	printer.write('6', align='center', font=("Courier", 14, "bold"))
	printer.home()
	printer.right(92.5)
	printer.forward(200)
	printer.write('3', align='center', font=("Courier", 14, "bold"))
	printer.left(2.5)
	printer.back(400)
	printer.write('9', align='center', font=("Courier", 14, "bold"))
	printer.home()
	turtle.tracer(True)
	# 100ms调用一次
	turtle.ontimer(lambda: startTick(second_hand, minute_hand, hour_hand, printer), 100)


'''开始运行时钟'''
def start():
	# 不显示绘制时钟的过程
	turtle.tracer(False)
	turtle.mode('logo')
	createHand('second_hand', 150)
	createHand('minute_hand', 125)
	createHand('hour_hand', 85)
	# 秒, 分, 时
	second_hand = turtle.Turtle()
	second_hand.shape('second_hand')
	minute_hand = turtle.Turtle()
	minute_hand.shape('minute_hand')
	hour_hand = turtle.Turtle()
	hour_hand.shape('hour_hand')
	for hand in [second_hand, minute_hand, hour_hand]:
		hand.shapesize(1, 1, 3)
		hand.speed(0)
	# 用于打印日期等文字
	printer = turtle.Turtle()
	printer.hideturtle()
	printer.penup()
	createClock(160)
	# 开始显示轨迹
	turtle.tracer(True)
	startTick(second_hand, minute_hand, hour_hand, printer)
	turtle.mainloop()


if __name__ == '__main__':
	start()