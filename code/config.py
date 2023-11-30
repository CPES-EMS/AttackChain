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