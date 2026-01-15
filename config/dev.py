"""
Mysql 数据库配置项
连接引擎官方文档：https://www.osgeo.cn/sqlalchemy/core/engines.html
数据库链接配置说明：mysql+asyncmy://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称
"""
# 数据库
SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:osinn123321@192.168.1.50:3306/osinn_vben"
# 任务调度连接数据库地址
APSCHEDULER_DATABASE_URL = "mysql+pymysql://root:osinn123321@192.168.1.50:3306/osinn_vben?charset=utf8"

"""
Redis 数据库配置
"""
REDIS_DB_ENABLE = True
# REDIS_DB_URL = "redis://:123456@177.8.0.5:6379/1"
REDIS_DB_CONFIG = {
    "host": "192.168.1.50",
    "port": 6379,
    "decode_responses": True,
    "db": 1
}

"""
是否开启定时任务调度
"""
APSCHEDULER_ENABLE = True
