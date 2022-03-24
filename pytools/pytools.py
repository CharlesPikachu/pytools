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


'''Python实用工具集'''
class pytools():
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.supported_tools = self.initialize()
        print(self)
    '''执行对应的小程序'''
    def execute(self, tool_type=None, config={}):
        assert tool_type in self.supported_tools, 'unsupport tool_type %s...' % tool_type
        qt_tools = [
            'newyearcardgenerator', 'luxunsentencesquery', 'artsigngenerator', 'genderpredictor', 'musicplayer', 'qrcodegenerator', 'videoplayer',
            'trumptweetsgenerator', 'coupletgenerator', 'idcardquery', 'idiomsolitaire', 'inquiryexpress', 'succulentquery', 'translator',
            'desktoppet', 'computersinger', 'hubbleseeonbirthday', 'ukrainemap'
        ]
        if tool_type in qt_tools:
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
            'timer': Timer, 'clock': Clock, 'runcat': RunCat, 'ukrainemap': UkraineMap,
            'desktoppet': DesktopPet, 'translator': Translator, 'calculator': Calculator, 'arxivhelper': ArxivHelper,
            'moviehelper': MovieHelper, 'videoplayer': VideoPlayer, 'musicplayer': MusicPlayer, 'idcardquery': IDCardQuery,
            'portscanner': PortScanner, 'playfireworks': PlayFireworks, 'emailsecurity': EmailSecurity, 'earthwallpaper': EarthWallpaper,
            'computersinger': ComputerSinger, 'inquiryexpress': InquiryExpress, 'idiomsolitaire': IdiomSolitaire, 'succulentquery': SucculentQuery,
            'iplocationquery': IPLocationQuery, 'genderpredictor': GenderPredictor, 'qrcodegenerator': QRCodeGenerator, 'coupletgenerator': CoupletGenerator,
            'artsigngenerator': ArtSignGenerator, 'controlpcbyemail': ControlPCbyEmail, 'naughtyconfession': NaughtyConfession, 'luxunsentencesquery': LuxunSentencesQuery,
            'hubbleseeonbirthday': HubbleSeeOnBirthday, 'newyearcardgenerator': NewYearCardGenerator, 'trumptweetsgenerator': TrumpTweetsGenerator,
        }
        return supported_tools
    '''获得所有支持的tools信息'''
    def getallsupported(self):
        all_supports = {}
        for key, value in self.supported_tools.items():
            all_supports[value.tool_name] = key
        return all_supports
    '''str'''
    def __str__(self):
        return 'Welcome to use Pytools!\nYou can visit https://github.com/CharlesPikachu/pytools for more details.'


'''run'''
if __name__ == '__main__':
    import random
    tool_client = pytools()
    all_supports = tool_client.getallsupported()
    tool_client.execute(random.choice(list(all_supports.values())))