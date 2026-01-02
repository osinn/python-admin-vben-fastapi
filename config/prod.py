"""
Mysql 数据库配置项
连接引擎官方文档：https://www.osgeo.cn/sqlalchemy/core/engines.html
数据库链接配置说明：mysql+asyncmy://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称
"""
SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:osinn123321@192.168.1.50:3306/tenant"