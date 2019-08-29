'''
Function:
	实现动态更新地球壁纸
Author:
	Charles
微信公众号:
	Charles的皮卡丘
'''
import os
import datetime
import requests
import win32gui, win32con, win32api


'''检查文件夹是否存在'''
def checkDir(dirname):
	if not os.path.exists(dirname):
		os.mkdir(dirname)


'''爬取壁纸'''
def crawlWallpaper(cache_dir='download'):
	checkDir(cache_dir)
	url_base = 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/'
	date = datetime.datetime.utcnow().strftime('%Y/%m/%d/')
	# 卫星图更新到网站上是有时延的
	hour = str(int(datetime.datetime.utcnow().strftime('%H')) - 1).zfill(2)
	minute = str(datetime.datetime.utcnow().strftime('%M'))[0] + '0'
	second = '00'
	ext = '_0_0.png'
	picture_url = url_base + date + hour + minute + second + ext
	res = requests.get(picture_url)
	with open(os.path.join(cache_dir, 'cache_wallpaper.png'), 'wb') as f:
		f.write(res.content)


'''换壁纸'''
def setWallPaper(imagepath='download/cache_wallpaper.png'):
	keyex = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
	win32api.RegSetValueEx(keyex, "WallpaperStyle", 0, win32con.REG_SZ, "0")
	win32api.RegSetValueEx(keyex, "TileWallpaper", 0, win32con.REG_SZ, "0")
	win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, imagepath, win32con.SPIF_SENDWININICHANGE)


'''主函数'''
def main():
	crawlWallpaper('download')
	setWallPaper(os.path.join(os.getcwd(), 'download/cache_wallpaper.png'))


'''run'''
if __name__ == '__main__':
	main()