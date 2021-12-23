'''
Function:
    翻译软件
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import os
import re
import time
import js2py
import random
import hashlib
import requests
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


'''百度js code'''
bd_js_code = r'''
function a(r) {
        if (Array.isArray(r)) {
            for (var o = 0, t = Array(r.length); o < r.length; o++)
                t[o] = r[o];
            return t
        }
        return Array.from(r)
    }
    function n(r, o) {
        for (var t = 0; t < o.length - 2; t += 3) {
            var a = o.charAt(t + 2);
            a = a >= "a" ? a.charCodeAt(0) - 87 : Number(a),
            a = "+" === o.charAt(t + 1) ? r >>> a : r << a,
            r = "+" === o.charAt(t) ? r + a & 4294967295 : r ^ a
        }
        return r
    }
    function e(r) {
        var o = r.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g);
        if (null === o) {
            var t = r.length;
            t > 30 && (r = "" + r.substr(0, 10) + r.substr(Math.floor(t / 2) - 5, 10) + r.substr(-10, 10))
        } else {
            for (var e = r.split(/[\uD800-\uDBFF][\uDC00-\uDFFF]/), C = 0, h = e.length, f = []; h > C; C++)
                "" !== e[C] && f.push.apply(f, a(e[C].split(""))),
                C !== h - 1 && f.push(o[C]);
            var g = f.length;
            g > 30 && (r = f.slice(0, 10).join("") + f.slice(Math.floor(g / 2) - 5, Math.floor(g / 2) + 5).join("") + f.slice(-10).join(""))
        }
        var u = void 0
          , l = "" + String.fromCharCode(103) + String.fromCharCode(116) + String.fromCharCode(107);
        u = null !== i ? i : (i = window[l] || "") || "";
        for (var d = u.split("."), m = Number(d[0]) || 0, s = Number(d[1]) || 0, S = [], c = 0, v = 0; v < r.length; v++) {
            var A = r.charCodeAt(v);
            128 > A ? S[c++] = A : (2048 > A ? S[c++] = A >> 6 | 192 : (55296 === (64512 & A) && v + 1 < r.length && 56320 === (64512 & r.charCodeAt(v + 1)) ? (A = 65536 + ((1023 & A) << 10) + (1023 & r.charCodeAt(++v)),
            S[c++] = A >> 18 | 240,
            S[c++] = A >> 12 & 63 | 128) : S[c++] = A >> 12 | 224,
            S[c++] = A >> 6 & 63 | 128),
            S[c++] = 63 & A | 128)
        }
        for (var p = m, F = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(97) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(54)), D = "" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(51) + ("" + String.fromCharCode(94) + String.fromCharCode(43) + String.fromCharCode(98)) + ("" + String.fromCharCode(43) + String.fromCharCode(45) + String.fromCharCode(102)), b = 0; b < S.length; b++)
            p += S[b],
            p = n(p, F);
        return p = n(p, D),
        p ^= s,
        0 > p && (p = (2147483647 & p) + 2147483648),
        p %= 1e6,
        p.toString() + "." + (p ^ m)
    }
'''


'''百度翻译软件'''
class BaiduTranslator():
    def __init__(self):
        self.session = requests.Session()
        self.session.cookies.set('BAIDUID', '19288887A223954909730262637D1DEB:FG=1;')
        self.session.cookies.set('PSTM', '%d;' % int(time.time()))
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }
        self.data = {
            'from': '', 'to': '', 'query': '', 'transtype': 'translang',
            'simple_means_flag': '3', 'sign': '', 'token': '', 'domain': 'common'
        }
        self.url = 'https://fanyi.baidu.com/v2transapi'
        self.langdetect_url = 'https://fanyi.baidu.com/langdetect'
    '''翻译'''
    def translate(self, word):
        self.data['from'] = self.detectLanguage(word)
        self.data['to'] = 'en' if self.data['from'] == 'zh' else 'zh'
        self.data['query'] = word
        self.data['token'], gtk = self.getTokenGtk()
        self.data['token'] = '6482f137ca44f07742b2677f5ffd39e1'
        self.data['sign'] = self.getSign(gtk, word)
        response = self.session.post(self.url, data=self.data)
        return [response.json()['trans_result']['data'][0]['result'][0][1]]
    '''获得token和gtk'''
    def getTokenGtk(self):
        url = 'https://fanyi.baidu.com/'
        response = requests.get(url, headers=self.headers)
        token = re.findall(r"token: '(.*?)'", response.text)[0]
        gtk = re.findall(r";window.gtk = ('.*?');", response.text)[0]
        return token, gtk
    '''获得签名'''
    def getSign(self, gtk, word):
        evaljs = js2py.EvalJs()
        js_code = bd_js_code
        js_code = js_code.replace('null !== i ? i : (i = window[l] || "") || ""', gtk)
        evaljs.execute(js_code)
        sign = evaljs.e(word)
        return sign
    '''检测使用的语言'''
    def detectLanguage(self, word):
        data = {'query': word}
        response = self.session.post(self.langdetect_url, headers=self.headers, data=data)
        return response.json()['lan']


'''有道翻译软件'''
class YoudaoTranslator():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Referer': 'http://fanyi.youdao.com/',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-481680322@10.169.0.83;'
        }
        self.data = {
            'i': None, 'from': 'AUTO', 'to': 'AUTO', 'smartresult': 'dict',
            'client': 'fanyideskweb', 'salt': None, 'sign': None, 'lts': None,
            'bv': None, 'doctype': 'json', 'version': '2.1', 'keyfrom': 'fanyi.web', 'action': 'FY_BY_REALTlME'
        }
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    '''翻译'''
    def translate(self, word):
        lts = str(int(time.time() * 10000))
        salt = lts + str(int(random.random() * 10))
        sign = 'fanyideskweb' + word + salt + 'Y2FYu%TNSbMCxc3t2u^XT'
        sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
        bv = '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        bv = hashlib.md5(bv.encode('utf-8')).hexdigest()
        self.data['i'] = word
        self.data['salt'] = salt
        self.data['sign'] = sign
        self.data['lts'] = lts
        self.data['bv'] = bv
        response = requests.post(self.url, headers=self.headers, data=self.data)
        return [response.json()['translateResult'][0][0].get('tgt')]


'''翻译软件'''
class Translator(QWidget):
    tool_name = '翻译软件'
    def __init__(self, parent=None, title='翻译软件 —— Charles的皮卡丘', **kwargs):
        super(Translator, self).__init__(parent)
        rootdir = os.path.split(os.path.abspath(__file__))[0]
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(os.path.join(rootdir, 'resources/icon.jpg')))
        # 定义组件
        self.label_ori = QLabel('原文')
        self.label_translated = QLabel('译文')
        self.lineedit_ori = QLineEdit()
        self.lineedit_translated = QLineEdit()
        self.btn_baidu = QPushButton()
        self.btn_youdao = QPushButton()
        self.btn_baidu.setText('百度翻译')
        self.btn_youdao.setText('有道翻译')
        # 布局
        self.grid = QGridLayout()
        self.grid.setSpacing(12)
        self.grid.addWidget(self.label_ori, 1, 0)
        self.grid.addWidget(self.lineedit_ori, 1, 1)
        self.grid.addWidget(self.label_translated, 2, 0)
        self.grid.addWidget(self.lineedit_translated, 2, 1)
        self.grid.addWidget(self.btn_baidu, 1, 2)
        self.grid.addWidget(self.btn_youdao, 2, 2)
        self.setLayout(self.grid)
        self.setFixedSize(400, 150)
        # 事件响应
        self.btn_baidu.clicked.connect(lambda : self.translate(api='baidu'))
        self.btn_youdao.clicked.connect(lambda : self.translate(api='youdao'))
        # 定义翻译软件
        self.bd_translate = BaiduTranslator()
        self.yd_translate = YoudaoTranslator()
    '''翻译'''
    def translate(self, api='baidu'):
        word = self.lineedit_ori.text()
        if not word: return
        if api == 'baidu': results = self.bd_translate.translate(word)
        elif api == 'youdao': results = self.yd_translate.translate(word)
        self.lineedit_translated.setText(';'.join(results))