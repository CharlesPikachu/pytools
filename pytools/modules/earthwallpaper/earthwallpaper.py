'''
Function:
    动态更新地球壁纸
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import datetime
import requests


'''动态更新地球壁纸'''
class EarthWallpaper():
    tool_name = '动态更新地球壁纸'
    def __init__(self, cache_dir='download', zoom_level=4, **kwargs):
        assert zoom_level >= 1 and zoom_level <= 20
        self.zoom_level = zoom_level
        self.cache_dir = cache_dir
    '''检查文件夹是否存在'''
    def checkdir(self, dirname):
        if not os.path.exists(dirname):
            os.mkdir(dirname)
    '''爬取壁纸'''
    def crawlWallpaper(self, cache_dir='download'):
        self.checkdir(cache_dir)
        latest_json_url = 'https://himawari8.nict.go.jp/img/D531106/latest.json'
        response = requests.get(latest_json_url)
        response_json = response.json()
        date = response_json['date']
        date, t = date.split(' ')
        date, t = date.replace('-', '/'), t.replace(':', '')
        url_base = 'https://himawari8.nict.go.jp/img/D531106/{}d/550/{}/{}_{}_{}.png'
        flag = False
        for i in range(self.zoom_level):
            for j in range(self.zoom_level):
                try:
                    picture_url = url_base.format(self.zoom_level, date, t, i, j)
                    response = requests.get(picture_url)
                    with open(os.path.join(cache_dir, 'cache_wallpaper.png'), 'wb') as f:
                        f.write(response.content)
                    flag = True
                except:
                    pass
                if flag: break
            if flag: break
    '''换壁纸'''
    def setWallPaper(self, imagepath='download/cache_wallpaper.png'):
        import win32gui, win32con, win32api
        keyex = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
        win32api.RegSetValueEx(keyex, "WallpaperStyle", 0, win32con.REG_SZ, "0")
        win32api.RegSetValueEx(keyex, "TileWallpaper", 0, win32con.REG_SZ, "0")
        win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, imagepath, win32con.SPIF_SENDWININICHANGE)
    '''运行'''
    def run(self):
        self.crawlWallpaper(self.cache_dir)
        self.setWallPaper(os.path.join(os.getcwd(), f'{self.cache_dir}/cache_wallpaper.png'))