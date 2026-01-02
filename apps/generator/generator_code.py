"""
数据库表生成 model
"""
import os
import re
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.engine import Inspector
from sqlalchemy.dialects.mysql import TINYINT
from jinja2 import Template

# ==================== 配置区 ====================
DATABASE_URL = "mysql+pymysql://root:osinn123321@192.168.1.50:3306/osinn_vben?charset=utf8"
DEFAULT_TABLE_NAME = "tbl_sys_user,tbl_role"
OUTPUT_PREFIX_REMOVE = "tbl_"
USE_MYSQL_BIGINT = True  # 设为 True 则 BIGINT 用 mysql.BIGINT
# =================================================

MODEL_TEMPLATE = '''from typing import Optional
from core.framework.database import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
{% if sql_imports %}from sqlalchemy import {{ sql_imports|join(', ') }}{% endif %}
{% if mysql_imports %}from sqlalchemy.dialects.mysql import {{ mysql_imports|join(', ') }}{% endif %}
{% if need_datetime or need_date or need_time %}
from datetime import {% if need_datetime %}datetime{% endif %}{% if need_date %}{% if need_datetime %}, {% endif %}date{% endif %}{% if need_time %}{% if need_datetime or need_date %}, {% endif %}time{% endif %}
{% endif %}

class {{ class_name }}(BaseEntity):
    __tablename__ = "{{ table_name }}"
{% for col in columns %}
    {{ col.name }}: Mapped[{% if col.py_type == 'str' %}str{% elif col.py_type == 'int' %}int{% elif col.py_type == 'bool' %}bool{% elif col.py_type == 'float' %}float{% elif col.py_type == 'datetime' %}datetime{% elif col.py_type == 'date' %}date{% elif col.py_type == 'time' %}time{% elif col.py_type == 'bytes' %}bytes{% elif col.py_type == 'dict' %}dict{% else %}Optional[{{ col.py_type }}]{% endif %}] = mapped_column({{ col.sql_type }}{% if col.primary_key %}, primary_key=True{% endif %}{% if not col.nullable %}, nullable=False{% endif %}{% if col.comment %}, comment="{{ col.comment|e }}"{% endif %})
{%- endfor %}
'''


def is_tinyint1(col_type_obj):
    """
    判断是否为 MySQL 的 TINYINT(1)
    利用 SQLAlchemy MySQL 方言的 display_width 属性
    """
    if isinstance(col_type_obj, TINYINT):
        display_width = getattr(col_type_obj, 'display_width', None)
        return display_width == 1
    return False


def map_to_sql_type(col_type_obj):
    # 先处理 TINYINT(1) → Boolean
    if is_tinyint1(col_type_obj):
        return 'Boolean'

    t_str = str(col_type_obj)
    t_upper = t_str.upper()

    if 'BIGINT' in t_upper:
        if USE_MYSQL_BIGINT:
            return 'BIGINT'
        else:
            return 'BigInteger'
    elif isinstance(col_type_obj, TINYINT):
        # 非 (1) 的 TINYINT 仍作为 Integer
        return 'Integer'
    elif 'INTEGER' in t_upper or ('INT' in t_upper and 'BIGINT' not in t_upper and 'SMALLINT' not in t_upper):
        return 'Integer'
    elif 'SMALLINT' in t_upper:
        return 'SmallInteger'
    elif 'VARCHAR' in t_upper or 'CHAR' in t_upper:
        match = re.search(r'\((\d+)\)', t_str)
        length = match.group(1) if match else '255'
        return f'String({length})'
    elif 'TEXT' in t_upper:
        return 'Text'
    elif 'BOOLEAN' in t_upper:
        return 'Boolean'
    elif 'FLOAT' in t_upper or 'DOUBLE' in t_upper:
        return 'Float'
    elif 'REAL' in t_upper:
        return 'Float'
    elif 'NUMERIC' in t_upper or 'DECIMAL' in t_upper:
        return 'Numeric'
    elif 'DATETIME' in t_upper or 'TIMESTAMP' in t_upper:
        return 'DateTime'
    elif 'DATE' in t_upper:
        return 'Date'
    elif 'TIME' in t_upper:
        return 'Time'
    elif 'JSON' in t_upper:
        return 'JSON'
    elif 'BLOB' in t_upper or 'BINARY' in t_upper:
        return 'LargeBinary'
    else:
        return 'String'


def map_to_python_type(col_type_obj):
    if is_tinyint1(col_type_obj):
        return 'bool'

    t = str(col_type_obj).upper()
    if 'INT' in t and 'BIGINT' not in t and 'SMALLINT' not in t and 'TINYINT' not in t:
        return 'int'
    elif 'BIGINT' in t or 'SMALLINT' in t or 'TINYINT' in t:
        return 'int'
    elif 'VARCHAR' in t or 'CHAR' in t or 'TEXT' in t:
        return 'str'
    elif 'BOOLEAN' in t:
        return 'bool'
    elif 'FLOAT' in t or 'REAL' in t or 'DOUBLE' in t or 'NUMERIC' in t or 'DECIMAL' in t:
        return 'float'
    elif 'DATETIME' in t or 'TIMESTAMP' in t:
        return 'datetime'
    elif 'DATE' in t:
        return 'date'
    elif 'TIME' in t:
        return 'time'
    elif 'JSON' in t:
        return 'dict'
    elif 'BLOB' in t or 'BINARY' in t:
        return 'bytes'
    else:
        return 'str'


def generate_model_code(table_name: str, engine):
    inspector = Inspector.from_engine(engine)
    columns_info = inspector.get_columns(table_name)

    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)
    pk_names = {c.name for c in table.primary_key.columns}

    columns = []
    sql_imports = set()
    mysql_imports = set()
    need_datetime = False
    need_date = False
    need_time = False

    for col in columns_info:
        name = col['name']
        col_type = col['type']
        nullable = col['nullable']
        comment = col.get('comment', None)

        sql_type = map_to_sql_type(col_type)
        py_type = map_to_python_type(col_type)

        # 导入管理
        if sql_type == 'BIGINT' and USE_MYSQL_BIGINT:
            mysql_imports.add('BIGINT')
        elif sql_type == 'BigInteger':
            sql_imports.add('BigInteger')
        elif sql_type == 'Integer':
            sql_imports.add('Integer')
        elif sql_type == 'SmallInteger':
            sql_imports.add('SmallInteger')
        elif 'String(' in sql_type:
            sql_imports.add('String')
        elif sql_type == 'Text':
            sql_imports.add('Text')
        elif sql_type == 'Boolean':
            sql_imports.add('Boolean')
        elif sql_type == 'Float':
            sql_imports.add('Float')
        elif sql_type == 'Numeric':
            sql_imports.add('Numeric')
        elif sql_type == 'DateTime':
            sql_imports.add('DateTime')
            need_datetime = True
        elif sql_type == 'Date':
            sql_imports.add('Date')
            need_date = True
        elif sql_type == 'Time':
            sql_imports.add('Time')
            need_time = True
        elif sql_type == 'JSON':
            sql_imports.add('JSON')
        elif sql_type == 'LargeBinary':
            sql_imports.add('LargeBinary')

        columns.append({
            'name': name,
            'sql_type': sql_type,
            'py_type': py_type,
            'primary_key': name in pk_names,
            'nullable': nullable,
            'comment': comment
        })

    clean_name = table_name[len(OUTPUT_PREFIX_REMOVE):] if table_name.startswith(OUTPUT_PREFIX_REMOVE) else table_name
    class_name = ''.join(word.capitalize() for word in clean_name.split('_'))

    template = Template(MODEL_TEMPLATE.strip())
    code = template.render(
        class_name=class_name + 'Model',
        table_name=table_name,
        columns=columns,
        sql_imports=sorted(sql_imports),
        mysql_imports=sorted(mysql_imports),
        need_datetime=need_datetime,
        need_date=need_date,
        need_time=need_time
    )
    return code


def main():
    #table_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TABLE_NAME
    engine = create_engine(DATABASE_URL)

    try:
        table_names = DEFAULT_TABLE_NAME.split(",")
        for table_name in table_names:
            code = generate_model_code(table_name, engine)
            output_base = table_name[len(OUTPUT_PREFIX_REMOVE):] if table_name.startswith(OUTPUT_PREFIX_REMOVE) else table_name
            output_file = os.path.join(os.getcwd(), f"{output_base}.py") # f"./{output_base}.py"

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(code)
            print(f"✅ 模型已生成：{output_file}")
    except Exception as e:
        print(f"❌ 生成失败：{e}")
        raise


if __name__ == "__main__":
    main()