# 安装Pytools


#### 环境配置

- 操作系统: Linux or macOS or Windows
- Python版本: Python3.6+
- Nodejs: 若需要使用translator等小工具, 需要安装最新版本的[Nodejs](https://nodejs.org/en/)。
- LAV Filters: 若需要在Windows上使用音乐播放器等小工具, 需要安装[LAV Filters](http://files.1f0.de/lavf/LAVFilters-0.65.exe)。


#### PIP安装(推荐)

在终端运行如下命令即可(请保证python在环境变量中):

```sh
pip install pikachupytools --upgrade
```


#### 源代码安装

**1.在线安装**

运行如下命令即可在线安装:

```sh
pip install git+https://github.com/CharlesPikachu/pytools.git@master
```

**2.离线安装**

利用如下命令下载pytools源代码到本地:

```sh
git clone https://github.com/CharlesPikachu/pytools.git
```

接着, 切到pytools目录下:

```sh
cd pytools
```

最后运行如下命令进行安装:

```sh
python setup.py install
```