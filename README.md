# python-admin-vben
python-admin-vben 后台管理系统，使用Python FastAPI 基于 vben5.0 版本，vue3 vite6 ant-design-vue typescript 语法开发高性能后台管理系统

> Python使用FastAPI框架示例，python 版本 >=3.13

# 安装依赖
- 执行`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
- 执行`pip freeze > requirements.txt`命令将项目依赖添加到`requirements.txt`中

# 接口文档
- http://127.0.0.1:8000/docs 或 http://127.0.0.1:8000/redoc

# sqlalchemy 参数速查表
| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `primary_key` | bool | 是否主键 | `primary_key=True` |
| `nullable` | bool | 是否允许NULL | `nullable=False` |
| `unique` | bool | 是否唯一 | `unique=True` |
| `index` | bool | 是否创建索引 | `index=True` |
| `default` | 任意 | Python默认值 | `default=0` |
| `server_default` | 字符串 | 数据库默认值 | `server_default='active'` |
| `onupdate` | 函数 | 更新时调用的函数 | `onupdate=datetime.utcnow` |
| `autoincrement` | bool/str | 自动增长 | `autoincrement=True` |
| `doc` | str | 文档字符串 | `doc='用户邮箱地址'` |
| `comment` | str | 列注释 | `comment='创建时间'` |
| `key` | str | Python属性名 | `key='user_name'` |
| `system` | bool | 是否为系统列 | `system=False` |