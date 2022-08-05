'''
Function:
    文件夹图标批量修改
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import stat


'''文件夹图标批量修改'''
class ModifyFolderICON():
    tool_name = '文件夹图标批量修改'
    def __init__(self, icon_path, **kwargs):
        assert os.path.exists(icon_path)
        self.icon_path = icon_path
    '''run'''
    def run(self):
        cur_dir = os.getcwd()
        for root, dirs, files in os.walk(os.getcwd(), topdown=False):
            os.chmod(root, stat.S_IREAD)
            for d in dirs:
                os.chdir(f'{os.path.join(root, d)}')
                if os.path.exists('desktop.ini'):
                    os.system('attrib -h -s desktop.ini')
                fp = open('desktop.ini', 'w')
                fp.write('[.ShellClassInfo]' + '\n' + f'IconResource={self.icon_path},0')
                fp.close()
                os.system('attrib +h desktop.ini')
                os.chdir(f'{cur_dir}')