# 1. 模型说明

模型简介：该模型主要用于在海量告警日志数据中快速挖掘潜在的链式告警行为，应用时序关联特征和告警间的拓扑连接关系，启发式搜索链式结构，辅助安全分析人员快速了解网络安全态势与威胁风险。



# 2. 代码环境依赖

代码开发与测试使用环境为Python3.7.6

```
matplotlib==3.7.1
networkx==3.1
numpy==1.24.3
pandas==2.0.2
pymysql==1.0.2
```

安装第三方库依赖使用`pip install -r requirements.txt`即可



# 3. 运行说明

运行程序：`python main.py`



## 配置文件

配置文件位于`code/config.py`，配置信息包含数据库连接信息，当前程序使用的输入输出是文件还是数据库，以及程序日志打印目录与文件名。

```
# 数据库连接信息
DB_SERVER="rm-2ze568o4qd438xw6cdo.mysql.rds.aliyuncs.com"  # 数据库主机地址
DB_PORT="3306"  # 数据库端口号
DB_USERNAME="ems"  # 数据库用户名
DB_PASSWORD="ems123@4"  # 数据库密码
DB_NAME="ems" # 数据库名
AttackChainTableName="attackchain" # 告警链数据表名

# 是否连接数据库
IS_CONNECT_DB=False  # 如果为False则从样例csv文件中读取，输出json文件，如果为True，则从数据库中读取并写入数据库

# 其他配置
LOG_FILE_DIR = 'log'
OUTPUT_FILE_NAME = 'output.json'
```



## 程序输入

通过修改配置文件中的配置项`IS_CONNECT_DB`来控制程序的输入来源，如果为False，则从样例输入文件`code/input.csv`中读取样例告警数据，如果为True，则从数据库中相应的数据表中读取告警数据。



## 程序输出

通过修改配置文件中的配置项`IS_CONNECT_DB`来控制程序的输出来源，如果为False，则将告警链挖掘结果以json形式存入配置项`OUTPUT_FILE_NAME`的文件中，如果为True，则将告警链挖掘结果写入告警链数据表。