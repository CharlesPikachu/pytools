'''
Function:
    羊了个羊小助手
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import time
import random
import requests


'''羊了个羊小助手'''
class SheepSheep():
    tool_name = '羊了个羊小助手'
    def __init__(self, user_t, **kwargs):
        self.headers = {
            'Host': 'cat-match.easygame2021.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.28(0x18001c27) NetType/WIFI Language/zh_CN',
            't': user_t,
            'Referer': 'https://servicewechat.com/wx141bfb9b73c970a9/17/page-frame.html',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'Connection': 'close',
        }
    '''运行'''
    def run(self):
        # 完成闯关羊群
        response = requests.get(f'https://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=1&rank_time={random.randint(1, 3600)}&rank_role=1&skin=1', headers=self.headers, timeout=10, verify=True)
        if response.json()['err_code'] == 0:
            self.logging('闯关羊群成功')
        else:
            self.logging(f'闯关羊群失败, 返回内容为:\n{response.json()}')
        # 完成闯关话题
        response = requests.get(f'https://cat-match.easygame2021.com/sheep/v1/game/topic_game_over?rank_score=1&rank_state=1&rank_time={random.randint(1, 3600)}&rank_role=2&skin=1', headers=self.headers, timeout=10, verify=True)
        if response.json()['err_code'] == 0:
            self.logging('闯关话题成功')
        else:
            self.logging(f'闯关话题失败, 返回内容为:\n{response.json()}')
    '''打印日志'''
    def logging(self, text):
        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} INFO]: {text}')