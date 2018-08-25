# 作者: Charles
# 公众号: Charles的皮卡丘
# 主函数
# 脚本仅供学习交流，禁止用于其他
import sys
from API import *


logo = r"""
  __  __            _
 |  \/  |          (_)
 | \  / | _____   ___  ___
 | |\/| |/ _ \ \ / / |/ _ \\
 | |  | | (_) \ V /| |  __/
 |_|  |_|\___/ \_/ |_|\___|
"""


def main():
	print('*' * 60)
	print(logo)
	print('[作者]: Charles')
	print('[公众号]: Charles的皮卡丘')
	print('[功能]: 电影小助手[电影查询|资源搜索]')
	print('[使用说明]: 根据输入提示输入正确的内容即可')
	print('[退出方式]: Ctrl + C')
	print('*' * 60)
	while True:
		print('请选择使用的功能(输入功能编号即可):\n[1].电影查询\n[2].电影资源搜索')
		choice = input('功能编号:')
		if choice == '1':
			keyword = input('请输入需要查询的电影名:')
			movies_info = douban.douban().search(keyword)
		elif choice == '2':
			keyword = input('请输入需要搜索的电影名:')
			while True:
				print('请输入搜索资源使用的平台号:\n[1].BT电影天堂\n[2].泡饭影视')
				platform = input('平台编号:')
				if platform == '1':
					link = resource.bt().search(keyword)
					break
				elif platform == '2':
					link = resource.paofan().search(keyword)
					break
				else:
					print('您的输入有误，请重新输入。')
		else:
			print('您的输入有误，请重新输入。')


if __name__ == '__main__':
	try:
		main()
	except:
		print('Bye...')
		sys.exit(0)