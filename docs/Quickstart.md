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
- **config中支持的参数**
```python
target_ip: 目标IP地址, 默认值"127.0.0.1"
port_min: 最小IP地址, 默认值"0"
port_max: 最大IP地址, 默认值"65535"
savedir: 扫描结果保存文件夹, 默认值"."
savename: 扫描结果保存文件名, 默认值"result.txt"
```