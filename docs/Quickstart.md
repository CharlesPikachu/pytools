# 快速开始


## 已经支持的小工具

#### 简易端口扫描器

**1.公众号文章链接**

暂无

**2.功能介绍**

简单的端口扫描工具。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('portscanner', config={'target_ip': '127.0.0.1'})
```

**4.config中支持的参数**

```
{
    target_ip: 目标IP地址, 默认值"127.0.0.1",
    port_min: 最小IP地址, 默认值"0",
    port_max: 最大IP地址, 默认值"65535",
    savedir: 扫描结果保存文件夹, 默认值".",
    savename: 扫描结果保存文件名, 默认值"result.txt",
}
```

#### 简易计时器

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/8HcXQjcsyegYzp_yt1cE5w)

**2.功能介绍**

简单的计时工具。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('timer')
```

**4.config中支持的参数**

```
{
    start_color: 开始计时的时候的字体颜色, 默认值"white",
    stop_color: 结束计时的时候的字体颜色, 默认值"red",
    title: 软件显示的标题, 默认值"简易计时器 —— Charles的皮卡丘",
}
```

#### 邮箱安全性验证工具

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/9u1CIa8MdoiXGGdPqae8fA)

**2.功能介绍** 

验证邮箱密码是否存在泄露。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('emailsecurity', config={'emails': ['1159254961@qq.com']})
```

**4.config中支持的参数**

```
{
    emails: 需要验证的emails列表, 默认值"['stevenlmh@163.com', 'hubeiyangyi@163.com', 'h465932675@163.com', 'xiajiahao456@163.com', 'zhangaorui1@163.com', 'babby126@163.com', 'a794685816@163.com', 'zzw67090@163.com', 'maye915@163.com', 'mao164951618@163.com', 'mczhoulei2011@163.com']",
    check_mode: 验证使用的网站, 目前支持"Firefox"和"Haveibeenpwned", 默认值为"Haveibeenpwned",
    hibp_api_key: 网站服务需要的api(需要自己购买), 默认值为"e0c4c2b5c7304030912b2251e15d7dac", 该key来源于网络,
}
```

#### 简易计算器

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/x6ygDEWHiYX10AP4y8e3MA)

**2.功能介绍** 

简单的计算器。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('calculator')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"简易计算器 —— Charles的皮卡丘",
    root_size: 软件大小, 默认值"(320, 420)",
}
```

#### 根据IP地址查询地理信息小工具

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/lYWxt00erojeSoyRWA1R5g)

**2.功能介绍** 

根据输入的IP地址查询地理坐标。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('iplocationquery', config={'ipaddress': '202.108.23.153'})
```

**4.config中支持的参数**

```
{
    ipaddress: 需要查询的IP地址, 默认值"202.108.23.153",
}
```

#### 简易时钟

**1.公众号文章链接**

[点击查看](https://mp.weixin.qq.com/s/8JPxEHGZ2u7dsEUJS-9WbQ)

**2.功能介绍** 

简单的时钟。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('clock')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"简易时钟 —— Charles的皮卡丘",
    time_deltas: 时分秒的偏移量, 默认值"(0, 0, 0)",
}
```

#### 快递查询系统

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/haNR8Yr9RsSXaTd0jl5PFA)

**2.功能介绍** 

根据快递单号查询快递。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('inquiryexpress')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"快递查询系统 —— Charles的皮卡丘",
}
```

#### 二维码生成器

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/XFmumQbQP4d9qf6HQBLVnA)

**2.功能介绍** 

根据输入文字生成二维码。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('qrcodegenerator')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"二维码生成器 —— Charles的皮卡丘",
}
```

#### 音乐播放器

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/SUyRNz_M7B6bcdV7-YxlZQ)

**2.功能介绍** 

简单的音乐播放器。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('musicplayer')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"音乐播放器 —— Charles的皮卡丘",
}
```

#### 鲁迅名言查询系统
**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/dQ8NfwFDoZw-6c1SPEl0aw)

**2.功能介绍** 

查询某句话鲁迅有没有说过。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('luxunsentencesquery')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"鲁迅名言查询系统 —— Charles的皮卡丘",
}
```

#### 奔跑的猫

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/8Fgzb8JiAoNSJqUanSi85Q)

**2.功能介绍** 

仿MAC上的奔跑的猫小软件。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('runcat')
```

**4.config中支持的参数**

```
{
    monitor_type: 监视类型, 支持"cpu"和"memory", 默认值"cpu",
}
```

#### 新年贺卡生成器

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/XCPkiXrKGZrVpNvyRlzgvA)

**2.功能介绍** 

生成新年贺卡的小软件。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('newyearcardgenerator')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"新年贺卡生成器 —— Charles的皮卡丘",
}
```

#### 仿抖音表白神器

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/wMxMrx07ZeOfYEXpuGYVsg)

**2.功能介绍**

仿抖音表白小软件。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('naughtyconfession')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"来自一位喜欢你的小哥哥",
}
```

#### 多肉数据查询系统

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/1_PzYVkMXwXrCiHBP5nZtQ)

**2.功能介绍**

查询多肉品种的小软件。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('succulentquery')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"多肉数据查询系统 —— Charles的皮卡丘",
}
```

#### 艺术签名生成器

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/CYxAgJZdEc87XIRcqWgRqw)

**2.功能介绍**

生成艺术签名的小软件。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('artsigngenerator')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"艺术签名生成器 —— Charles的皮卡丘",
}
```

#### 给定中文名的性别猜测器

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/NS3DfRpIfw5wFsV3EaqEzQ)

**2.功能介绍**

给定中文名，判断性别的小软件。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('genderpredictor')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"给定中文名的性别猜测器 —— Charles的皮卡丘",
}
```

#### 成语接龙小软件

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/ncgl2OBUZsE77gOy1gclYg)

**2.功能介绍**

成语接龙小软件。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('idiomsolitaire')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"成语接龙小软件 —— Charles的皮卡丘",
}
```

#### 特朗普推特生成器

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/KO_nWpejIqQNKZgbCBfWEQ)

**2.功能介绍**

生成特朗普风格的推特的小软件。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('trumptweetsgenerator')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"特朗普推特生成器 —— Charles的皮卡丘",
}
```

#### 身份证信息查询工具

**1.公众号文章链接**

[点击查看](https://mp.weixin.qq.com/s/2zljIGm-5WlRCq68ADXSiw)

**2.功能介绍**

根据身份证号推断个人信息的小软件。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('idcardquery')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"身份证信息查询工具 —— Charles的皮卡丘",
}
```

#### 视频播放器

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/pG6SwhfNSWZuHxuMcEQZog)

**2.功能介绍**

简单的视频播放器。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('videoplayer')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"视频播放器 —— Charles的皮卡丘",
}
```

#### 春联生成器

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/L1gmiMJ-M8T-QgSeJckYEw)

**2.功能介绍**

根据主题自动生成春联的小软件。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('coupletgenerator')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"春联生成器 —— Charles的皮卡丘",
    api_key: https://console.bce.baidu.com/#/index/overview申请到的对联生成器所需的api_key,
    secret_key: https://console.bce.baidu.com/#/index/overview申请到的对联生成器所需的secret_key,
}
```

#### 翻译软件

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/SWR-bUdqfpn3NxR5OgCYlg)

**2.功能介绍**

简单的翻译软件。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('translator')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"翻译软件 —— Charles的皮卡丘",
}
```

#### 桌面宠物

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/4kOzdRXmrxzR88QcYYSFvQ)

**2.功能介绍**

简单的桌面宠物, 有皮卡丘。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('desktoppet')
```

**4.config中支持的参数**

```
{
    ACTION_DISTRIBUTION: 连贯动作的图片索引, 默认值"[['1', '2', '3'], ['4', '5', '6', '7', '8', '9', '10', '11'], ...]",
    PET_ACTIONS_MAP: 宠物素材路径, 默认值"{'pet_1': ACTION_DISTRIBUTION}",
    pet_type: 指定宠物类型, 支持'bingdwendwen', 'pikachu', 'fox', 'blackcat'和'whitecat',
}
```

#### 让电脑主板上的蜂鸣器哼歌

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/-yT1NxAUTN8hzZs76qzqjQ)

**2.功能介绍**

让电脑主板上的蜂鸣器哼歌。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('computersinger')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"让电脑主板上的蜂鸣器哼歌 —— Charles的皮卡丘",
}
```

#### 你生日那天的宇宙

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/hJDcRHNHT1Zc0akctvWqsA)

**2.功能介绍**

查看你生日那天哈勃望远镜拍到的宇宙。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('hubbleseeonbirthday')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"你生日那天的宇宙 —— Charles的皮卡丘",
}
```

#### 动态更新地球壁纸

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/pDZpzzpd1g5bodtFdEROEg)

**2.功能介绍**

将当前卫星拍到的照片设置为电脑壁纸。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('earthwallpaper')
```

**4.config中支持的参数**

```
{
    cache_dir: 缓存文件夹, 默认值"download",
    zoom_level: 缩放比例, 默认值"4",
}
```

#### 电影小助手

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/VlwCyD99YBYhIbwG4rYN3A)

**2.功能介绍**

电影查询小工具。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('moviehelper')
```

**4.config中支持的参数**

```python
暂无
```

#### 邮件控制电脑

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/KnG-mncegaB35v5THAUJXQ)

**2.功能介绍**

利用邮件远程控制电脑。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('controlpcbyemail')
```

**4.config中支持的参数**

```python
time_interval: 失败重复尝试次数, 默认值"5"
options: 选项, 默认值
{
    "sender": {
        "email": "xxx@qq.com"
    },
    "receiver": {
        "email": "xxx@sina.com",
        "password": "",
        "pop3_server": "pop.sina.com",
        "smtp_server": "smtp.sina.com",
        "enable_ssl": false,
        "port": 0,
	}
}
word2cmd_dict: 命令字典, 默认值
{
    "关机": "shutdown -s -t 00",
    "取消关机": "shutdown -a",
    "锁屏": "rundll32.exe user32.dll,LockWorkStation",
    "截屏": "screenshot",
}
```

#### 放烟花特效

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/wzz_7gKIt7iU-7kM_9o_pw)

**2.功能介绍**

实现放烟花特效。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('playfireworks')
```

**4.config中支持的参数**

```python
暂无
```

#### Arxiv小助手

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/XypPxlWmzbRoEEEhusEXJA)

**2.功能介绍**

定时给自己推送arxiv上自己感兴趣的论文。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('arxivhelper', config={'time_interval': 3600*5, 'server_key': 'SCT118858TwORPoXsvuaPP1Cri50qkUpOf', 'keywords_list': ['continual learning']})
```

**4.config中支持的参数**

```python
{
    time_interval: 每隔多少秒搜索一次arxiv，默认值为5*3600秒, 即5小时,
    server_key: server酱的key值，到http://sc.ftqq.com/3.version申请即可, 默认值为None,
    keywords_list: 我们感兴趣的论文关键字列表, 默认值为['continual learning'],
    history_filename: 缓存文件, 默认值为'cache.pkl',
}
```

#### 乌克兰地图查询系统

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/zthIMtWqF7mJiIlXy1-bsA)

**2.功能介绍**

简单的乌克兰地图查询系统。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('ukrainemap')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"乌克兰地图查询系统 —— Charles的皮卡丘",
}
```

#### 苏联笑话生成器

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/PUTJxDLpCVRSaUzvarizEQ)

**2.功能介绍**

简单的苏联笑话生成器。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('sovietgenerator')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"苏联笑话生成器 —— Charles的皮卡丘",
}
```

#### 稳中向好生成器

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/mH9LyIdHe1uX2E3oAjlIoQ)

**2.功能介绍**

简单的稳中向好生成器。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('goodgoodgenerator')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"稳中向好生成器 —— Charles的皮卡丘",
}
```

#### 天眼查

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/IpaOCq1600JyIf9QWieoTQ)

**2.功能介绍**

天眼查GUI版本。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('tianyancha')
```

**4.config中支持的参数**

```
{
    title: 软件显示的标题, 默认值"天眼查 —— Charles的皮卡丘",
}
```

#### 盗取浏览器里的账号密码

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/sotiVBWrFxcyYAgdRJ5ydA)

**2.功能介绍**

盗取浏览器里的账号密码。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('decryptbrowser')
```

**4.config中支持的参数**

```
{
    savename: 保存盗取的账号密码的文件名, 默认值为"results.csv",
}
```

#### 国内访问Github一键加速脚本

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/OEWi5y_AbM1jE526LCp4aw)

**2.功能介绍**

国内访问Github一键加速脚本。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('githubacceleration')
```

**4.config中支持的参数**

```
{
    domains: Github相关的域名列表, 默认为"None", 即自动生成, 
    hosts_path: 需要修改的hosts文件路径, 默认为"None", 即自动生成, 
    proxies: 抓取域名对应的IP地址时使用的代理,
}
```

#### 文件夹图标批量修改

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/40QlSkwQ-ezpeDiPWlkUAg)

**2.功能介绍**

文件夹图标批量修改。

**3.调用示例代码**

```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('modifyfoldericon', config={'icon_path': r'D:\icon.ico'})
```

**4.config中支持的参数**

```
{
    icon_path: 目标图标路径, 
}
```

#### "羊了个羊"小助手

**1.公众号文章链接** 

[点击查看](https://mp.weixin.qq.com/s/Kj0s67IaNzU9s0ywAmNayg)

**2.功能介绍**

"羊了个羊"小助手。

**3.调用示例代码**

```python
from pytools import pytools
​
tool_client = pytools.pytools()
tool_client.execute('sheepsheep', {'user_t': 'xxx'})
```

**4.config中支持的参数**

```
{
    user_t: 每个用户特有的t值, 需要自己抓包获取, 
}
```


## 随机运行一个小程序

写如下代码，保存并运行即可：

```python
import random
from pytools import pytools

tool_client = pytools.pytools()
all_supports = tool_client.getallsupported()
tool_client.execute(random.choice(list(all_supports.values())))
```