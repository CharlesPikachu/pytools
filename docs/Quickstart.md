# 快速开始


## 已经支持的小工具

#### 简易端口扫描器
- 历史文章链接: 暂无
- 功能介绍: 简单的端口扫描工具
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('portscanner', config={'target_ip': '127.0.0.1'})
```
- config中支持的参数
```python
target_ip: 目标IP地址, 默认值"127.0.0.1"
port_min: 最小IP地址, 默认值"0"
port_max: 最大IP地址, 默认值"65535"
savedir: 扫描结果保存文件夹, 默认值"."
savename: 扫描结果保存文件名, 默认值"result.txt"
```

#### 简易计时器
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/8HcXQjcsyegYzp_yt1cE5w)
- 功能介绍: 简单的计时工具
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('timer')
```
- config中支持的参数
```python
start_color: 开始计时的时候的字体颜色, 默认值"white"
stop_color: 结束计时的时候的字体颜色, 默认值"red"
title: 软件显示的标题, 默认值"简易计时器 —— Charles的皮卡丘"
```

#### 邮箱安全性验证工具
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/9u1CIa8MdoiXGGdPqae8fA)
- 功能介绍: 验证邮箱密码是否存在泄露
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('emailsecurity', config={'emails': ['1159254961@qq.com']})
```
- config中支持的参数
```python
emails: 需要验证的emails列表, 默认值"['stevenlmh@163.com', 'hubeiyangyi@163.com', 'h465932675@163.com', 'xiajiahao456@163.com', 'zhangaorui1@163.com', 'babby126@163.com', 'a794685816@163.com', 'zzw67090@163.com', 'maye915@163.com', 'mao164951618@163.com', 'mczhoulei2011@163.com']"
check_mode: 验证使用的网站, 目前支持"Firefox"和"Haveibeenpwned", 默认值为"Haveibeenpwned"
hibp_api_key: 网站服务需要的api(需要自己购买), 默认值为"e0c4c2b5c7304030912b2251e15d7dac", 该key来源于网络
```

#### 简易计算器
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/x6ygDEWHiYX10AP4y8e3MA)
- 功能介绍: 简单的计算器
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('calculator')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"简易计算器 —— Charles的皮卡丘"
root_size: 软件大小, 默认值"(320, 420)"
```

#### 根据IP地址查询地理信息小工具
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/lYWxt00erojeSoyRWA1R5g)
- 功能介绍: 根据输入的IP地址查询地理坐标
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('iplocationquery', config={'ipaddress': '202.108.23.153'})
```
- config中支持的参数
```python
ipaddress: 需要查询的IP地址, 默认值"202.108.23.153"
```

#### 简易时钟
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/8JPxEHGZ2u7dsEUJS-9WbQ)
- 功能介绍: 简单的时钟
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('clock')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"简易时钟 —— Charles的皮卡丘"
time_deltas: 时分秒的偏移量, 默认值"(0, 0, 0)"
```

#### 快递查询系统
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/haNR8Yr9RsSXaTd0jl5PFA)
- 功能介绍: 根据快递单号查询快递
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('inquiryexpress')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"快递查询系统 —— Charles的皮卡丘"
```

#### 二维码生成器
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/XFmumQbQP4d9qf6HQBLVnA)
- 功能介绍: 根据输入文字生成二维码
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('qrcodegenerator')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"二维码生成器 —— Charles的皮卡丘"
```

#### 音乐播放器
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/SUyRNz_M7B6bcdV7-YxlZQ)
- 功能介绍: 简单的音乐播放器
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('musicplayer')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"音乐播放器 —— Charles的皮卡丘"
```

#### 鲁迅名言查询系统
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/dQ8NfwFDoZw-6c1SPEl0aw)
- 功能介绍: 查询某句话鲁迅有没有说过
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('luxunsentencesquery')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"鲁迅名言查询系统 —— Charles的皮卡丘"
```

#### 奔跑的猫
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/8Fgzb8JiAoNSJqUanSi85Q)
- 功能介绍: 仿MAC上的奔跑的猫小软件
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('runcat')
```
- config中支持的参数
```python
monitor_type: 监视类型, 支持"cpu"和"memory", 默认值"cpu"
```

#### 新年贺卡生成器
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/XCPkiXrKGZrVpNvyRlzgvA)
- 功能介绍: 生成新年贺卡的小软件
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('newyearcardgenerator')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"新年贺卡生成器 —— Charles的皮卡丘"
```

#### 仿抖音表白神器
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/wMxMrx07ZeOfYEXpuGYVsg)
- 功能介绍: 仿抖音表白小软件
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('naughtyconfession')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"来自一位喜欢你的小哥哥"
```

#### 多肉数据查询系统
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/1_PzYVkMXwXrCiHBP5nZtQ)
- 功能介绍: 查询多肉品种的小软件
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('succulentquery')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"多肉数据查询系统 —— Charles的皮卡丘"
```

#### 艺术签名生成器
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/CYxAgJZdEc87XIRcqWgRqw)
- 功能介绍: 生成艺术签名的小软件
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('artsigngenerator')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"艺术签名生成器 —— Charles的皮卡丘"
```

#### 给定中文名的性别猜测器
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/NS3DfRpIfw5wFsV3EaqEzQ)
- 功能介绍: 给定中文名，判断性别的小软件
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('genderpredictor')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"给定中文名的性别猜测器 —— Charles的皮卡丘"
```

#### 成语接龙小软件
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/ncgl2OBUZsE77gOy1gclYg)
- 功能介绍: 成语接龙小软件
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('idiomsolitaire')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"成语接龙小软件 —— Charles的皮卡丘"
```

#### 特朗普推特生成器
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/KO_nWpejIqQNKZgbCBfWEQ)
- 功能介绍: 生成特朗普风格的推特的小软件
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('trumptweetsgenerator')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"特朗普推特生成器 —— Charles的皮卡丘"
```

#### 身份证信息查询工具
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/2zljIGm-5WlRCq68ADXSiw)
- 功能介绍: 根据身份证号推断个人信息的小软件
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('idcardquery')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"身份证信息查询工具 —— Charles的皮卡丘"
```

#### 视频播放器
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/pG6SwhfNSWZuHxuMcEQZog)
- 功能介绍: 简单的视频播放器
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('videoplayer')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"视频播放器 —— Charles的皮卡丘"
```

#### 春联生成器
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/L1gmiMJ-M8T-QgSeJckYEw)
- 功能介绍: 根据主题自动生成春联的小软件
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('coupletgenerator')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"春联生成器 —— Charles的皮卡丘"
api_key: https://console.bce.baidu.com/#/index/overview申请到的对联生成器所需的api_key
secret_key: https://console.bce.baidu.com/#/index/overview申请到的对联生成器所需的secret_key
```

#### 翻译软件
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/SWR-bUdqfpn3NxR5OgCYlg)
- 功能介绍: 简单的翻译软件
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('translator')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"翻译软件 —— Charles的皮卡丘"
```

#### 桌面宠物
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/4kOzdRXmrxzR88QcYYSFvQ)
- 功能介绍: 简单的桌面宠物, 有皮卡丘
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('desktoppet')
```
- config中支持的参数
```python
ACTION_DISTRIBUTION: 连贯动作的图片索引, 默认值"[['1', '2', '3'], ['4', '5', '6', '7', '8', '9', '10', '11'], ...]"
PET_ACTIONS_MAP: 宠物素材路径, 默认值"{'pet_1': ACTION_DISTRIBUTION}"
```

#### 让电脑主板上的蜂鸣器哼歌
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/-yT1NxAUTN8hzZs76qzqjQ)
- 功能介绍: 让电脑主板上的蜂鸣器哼歌
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('computersinger')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"让电脑主板上的蜂鸣器哼歌 —— Charles的皮卡丘"
```

#### 你生日那天的宇宙
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/hJDcRHNHT1Zc0akctvWqsA)
- 功能介绍: 查看你生日那天哈勃望远镜拍到的宇宙
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('hubbleseeonbirthday')
```
- config中支持的参数
```python
title: 软件显示的标题, 默认值"你生日那天的宇宙 —— Charles的皮卡丘"
```

#### 动态更新地球壁纸
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/pDZpzzpd1g5bodtFdEROEg)
- 功能介绍: 将当前卫星拍到的照片设置为电脑壁纸
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('earthwallpaper')
```
- config中支持的参数
```python
cache_dir: 缓存文件夹, 默认值"download"
zoom_level: 缩放比例, 默认值"4"
```

#### 电影小助手
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/VlwCyD99YBYhIbwG4rYN3A)
- 功能介绍: 电影查询小工具
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('moviehelper')
```
- config中支持的参数
```python
暂无
```

#### 邮件控制电脑
- 历史文章链接: [点击查看](https://mp.weixin.qq.com/s/KnG-mncegaB35v5THAUJXQ)
- 功能介绍: 利用邮件远程控制电脑
- 调用示例代码:
```python
from pytools import pytools

tool_client = pytools.pytools()
tool_client.execute('controlpcbyemail')
```
- config中支持的参数
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
		"port": 0
	}
}
word2cmd_dict: 命令字典, 默认值
{
	"关机": "shutdown -s -t 00",
	"取消关机": "shutdown -a",
	"锁屏": "rundll32.exe user32.dll,LockWorkStation",
	"截屏": "screenshot"
}
```