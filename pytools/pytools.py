'''
Function:
    Python实用工具集
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import warnings
from PyQt5.QtWidgets import QApplication
if __name__ == '__main__':
    from modules import *
    from __init__ import __version__
else:
    from .modules import *
    from .__init__ import __version__
warnings.filterwarnings('ignore')


'''basic info'''
BASICINFO = '''************************************************************
Function: Python实用工具集 V%s
Author: Charles
微信公众号: Charles的皮卡丘
操作帮助:
    输入r: 重新初始化程序(即返回主菜单)
    输入q: 退出程序
视频保存路径:
    当前路径下的%s文件夹内
************************************************************'''


'''Python实用工具集'''
class pytools():
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.supported_tools = self.initialize()
    '''执行对应的小程序'''
    def execute(self, tool_type=None, config={}):
        assert tool_type in self.supported_tools, 'unsupport tool_type %s...' % tool_type
        if tool_type in ['luxunsentencesquery', 'artsigngenerator']:
            app = QApplication(sys.argv)
            client = self.supported_tools[tool_type](**config)
            client.show()
            sys.exit(app.exec_())
        else:
            client = self.supported_tools[tool_type](**config)
            client.run()
    '''初始化'''
    def initialize(self):
        supported_tools = {
            'timer': Timer,
            'clock': Clock,
            'calculator': Calculator,
            'portscanner': PortScanner,
            'emailsecurity': EmailSecurity,
            'artsigngenerator': ArtSignGenerator,
            'luxunsentencesquery': LuxunSentencesQuery,
        }
        return supported_tools
    '''获得所有支持的tools信息'''
    def getallsupported(self):
        all_supports = {}
        for key, value in self.supported_tools.items():
            all_supports[value.tool_name] = key
        return all_supports


'''run'''
if __name__ == '__main__':
    tool_client = pytools()
    print(tool_client.getallsupported())
    tool_client.execute('artsigngenerator')