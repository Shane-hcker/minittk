# MiniTTK + Automation App

**搭建minittk框架并且实现一个登入会议+数据管理的小工具**

## 为什么? 有什么功能?

### Why:

本人为初中生，考虑到上网课时进入会议那些繁琐的操作，自己一心想从重复性劳动中解脱，因而写了个Minittk优化质量节省时间，再用该框架开发出了一个小工具，希望能帮助很多人:smile:

### Features:

- **Minittk**
  - 类`Window`
    - 用于创建TopLevel/Window窗口, 内部封装了一些常用函数
  - 抽象类 `support.BaseConnection(pymysql.Connection)`
    - 里面包含相关函数定义的规范, 用于连接到MySQL数据库，详细用途见<a href='#env'>下文</a>
  - 单例 `support.UserConnection(BaseConnection)`
    - 派生于`BaseConnection`，里面包含了使用入会小工具的所有数据库操作的函数
  - 单例 `support.MyConfigParser(configparser.ConfigParser)`
    - 用于读写`.ini`文件, 里面对访问或者导入保存文件等操作进行了部分封装
- **App**
  - 

<h2 id='env'>环境配置</h2>

Python 3.10.4 (or above(?))

### 安装第三方库:

**ttkbootstrap:**

```
pip install ttkbootstrap
```

**pymysql:**

```
pip install pymysql
```

**configparser:**

```
pip install configparser
```

