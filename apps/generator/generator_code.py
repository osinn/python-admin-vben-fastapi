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
DEFAULT_TABLE_NAME = "tbl_sys_notice"
OUTPUT_PREFIX_REMOVE = "tbl_"
USE_MYSQL_BIGINT = True  # 设为 True 则 BIGINT 用 mysql.BIGINT
folders = ['crud', 'models', 'params', 'routers', 'schemas']
# =================================================

MODEL_TEMPLATE = '''from typing import Optional
from core.framework.database import BaseEntity
from sqlalchemy.orm import Mapped, mapped_column
{% if sql_imports %}from sqlalchemy import {{ sql_imports|join(', ') }}{% endif %}
{% if mysql_imports %}from sqlalchemy.dialects.mysql import {{ mysql_imports|join(', ') }}{% endif %}
{% if need_datetime or need_date or need_time %}
from datetime import {% if need_datetime %}datetime{% endif %}{% if need_date %}{% if need_datetime %}, {% endif %}date{% endif %}{% if need_time %}{% if need_datetime or need_date %}, {% endif %}time{% endif %}
{% endif %}

{% set skip_fields = ['id', 'created_by', 'created_time', 'updated_by', 'updated_time', 'is_deleted'] %}

class {{ class_name }}(BaseEntity):
    __tablename__ = "{{ table_name }}"
{% for col in columns %}
    {%- if col.name not in skip_fields %}
    {{ col.name }}: Mapped[{% if col.py_type == 'str' %}str{% elif col.py_type == 'int' %}int{% elif col.py_type == 'bool' %}bool{% elif col.py_type == 'float' %}float{% elif col.py_type == 'datetime' %}datetime{% elif col.py_type == 'date' %}date{% elif col.py_type == 'time' %}time{% elif col.py_type == 'bytes' %}bytes{% elif col.py_type == 'dict' %}dict{% else %}Optional[{{ col.py_type }}]{% endif %}] = mapped_column({{ col.sql_type }}{% if col.primary_key %}, primary_key=True{% endif %}{% if not col.nullable %}, nullable=False{% endif %}{% if col.comment %}, comment="{{ col.comment|e }}"{% endif %})
    {%- endif %}
{%- endfor %}
'''
SCHEMA_TEMPLATE = '''from typing import Optional
from pydantic import Field
from core.framework.common_schemas import BaseSchema
{% if need_datetime or need_date or need_time %}
from datetime import {% if need_datetime %}datetime{% endif %}{% if need_date %}{% if need_datetime %}, {% endif %}date{% endif %}{% if need_time %}{% if need_datetime or need_date %}, {% endif %}time{% endif %}
{% endif %}

{% set skip_fields = ['id', 'created_by', 'created_time', 'updated_by', 'updated_time', 'is_deleted'] %}

class {{ class_name }}Schema(BaseSchema):
{% for col in columns %}
    {%- if col.name not in skip_fields %}
    {{ col.name }}: Optional[{% if col.py_type == 'str' %}str{% elif col.py_type == 'int' %}int{% elif col.py_type == 'bool' %}bool{% elif col.py_type == 'float' %}float{% elif col.py_type == 'datetime' %}datetime{% elif col.py_type == 'date' %}date{% elif col.py_type == 'time' %}time{% elif col.py_type == 'bytes' %}bytes{% elif col.py_type == 'dict' %}dict{% else %}Optional[{{ col.py_type }}]{% endif %}] = Field(default=None{% if col.comment %}, description="{{ col.comment|e }}"{% endif %})
    {%- endif %}
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

def generate_schema_code():
    print('')

def create_project_structure(table_name, name, class_name):
    """
    创建项目文件夹结构
    router_names: 要创建的router文件名列表，不包含_router.py后缀
    """
    # 定义要创建的文件夹列表

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        # from .sys_notice_router import sys_notice_router
        if folder == 'params':
            with open(os.path.join(folder,  f"{name}.py"), 'w', encoding='utf-8') as f:
                f.write('from pydantic import Field\n')
                f.write('from core.framework.common_schemas import BaseModelSchema\n\n')
                f.write(f'class {class_name}PageParam(BaseModelSchema):\n'
                        '    page_num: int = Field(default=1, description="当前页，默认1（从1开始）")\n'
                        '    page_size: int = Field(default=10, description="每页行数，默认10")\n'
                        '    search_key: Optional[str] = Field(default=None, description="搜索关键字：")\n')
                f.write(f'\nclass {class_name}AddParam(BaseModelSchema):\n')
                f.write('    pass\n')
                f.write(f'\nclass {class_name}EditParam({class_name}AddParam):\n')
                f.write('    id: int = Field(description="唯一ID")\n')

        if folder == 'crud':
            with open(os.path.join(folder,  f"crud_{name}.py"), 'w', encoding='utf-8') as f:
                f.write(f'from core.framework.crud_async_session import AsyncGenericCRUD\n')
                f.write(f'\nasync def page_query_{name}_list(param: {class_name}PageParam, crud_async_session: AsyncGenericCRUD):\n')
                f.write(f'    sql = ["select * from {table_name} where is_deleted = 0"]\n')
                f.write(f'    sql.append(" order by created_time desc")\n')
                f.write(f'    page_vo = await crud_async_session.page_select_model(" ".join(sql), param.__dict__, v_schema={class_name}Schema)\n')
                f.write(f'    return page_vo\n')

        init_file = os.path.join(folder, '__init__.py')
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(f'# {folder.capitalize()} module\n')
            f.write('# Auto-generated __init__.py\n')
            if folder == 'routers':
                f.write(f'from .{name}_router import {name}_router\n')


        print(f"✓ {folder}/")

    filename = f"{name}_router.py"
    filepath = os.path.join('routers', filename)
    class_name_model = class_name + 'Model'
    # 写入路由文件内容
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('from fastapi import APIRouter, Depends, Path\n')
        f.write('from core.framework.crud_async_session import crud_getter, AsyncGenericCRUD\n')
        f.write('from core.framework.response import SuccessResponse, ErrorResponse\n')
        f.write('\n')
        f.write(f'{name}_router = APIRouter()\n')
        f.write('\n')
        f.write(f'@{name}_router.post("/get_{name}_list", summary="列表查询")\n')
        f.write(f'async def get_{name}s(param: {class_name}PageParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter({class_name_model}))):\n')
        f.write(f'    """获取所有{name}"""\n')
        f.write(f'    page_vo = await page_query_{name}_list(param, crud_async_session)\n')
        f.write(f'    await crud_async_session.fill_base_user_info(page_vo.items)\n')
        f.write(f'    return SuccessResponse(page_vo)\n')
        f.write('\n')
        f.write(f'@{name}_router.post("/add_{name}", summary="新增数据")\n')
        f.write(f'async def add_{name}(param: {class_name}AddParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter({class_name_model}))):\n')
        f.write(f'    """创建新的{name}"""\n')
        f.write(f'    await crud_async_session.create(param)\n')
        f.write(f'    return SuccessResponse("OK")\n')
        f.write('\n')
        f.write(f'@{name}_router.get("/{{{name}_id}}/get_{name}_info", summary="获取详情")\n')
        f.write(f'async def get_{name}({name}_id: int = Path(description="唯一ID"), crud_async_session: AsyncGenericCRUD = Depends(crud_getter({class_name_model}))):\n')
        f.write(f'    """根据ID获取{name}"""\n')
        f.write(f'    return SuccessResponse(await crud_async_session.get(sys_notice_id, v_schema={class_name}Schema))\n')
        f.write('\n')
        f.write(f'@{name}_router.put("/edit_{name}", summary="编辑数据")\n')
        f.write(f'async def edit_{name}(param: {class_name}EditParam, crud_async_session: AsyncGenericCRUD = Depends(crud_getter({class_name_model}))):\n')
        f.write(f'    """更新{name}"""\n')
        f.write(f'    db_obj = await crud_async_session.get(param.id)\n')
        f.write(f'    if not db_obj:\n')
        f.write(f'        return ErrorResponse("数据不存在")\n')
        f.write(f'    await crud_async_session.update(param, db_obj)\n')
        f.write(f'    return SuccessResponse("OK")\n')
        f.write('\n')
        f.write(f'@{name}_router.delete("/{{{name}_id}}/delete_{name}", summary="删除数据")\n')
        f.write(f'async def delete_{name}({name}_id: int = Path(description="唯一ID"), crud_async_session: AsyncGenericCRUD = Depends(crud_getter({class_name_model}))):\n')
        f.write(f'    """删除{name}"""\n')
        f.write(f'    result: bool = await crud_async_session.delete(sys_notice_id)\n')
        f.write(f'    if not result:\n')
        f.write(f'        return ErrorResponse("删除失败")\n')
        f.write(f'    return SuccessResponse("OK")\n')

    print(f"\n项目结构创建完成！")

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

    output_base = table_name[len(OUTPUT_PREFIX_REMOVE):] if table_name.startswith(OUTPUT_PREFIX_REMOVE) else table_name

    create_project_structure(table_name, output_base, class_name)

    output_file = os.path.join(os.getcwd(), f"{folders[1]}/{output_base}.py")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"✅ model已生成：{output_file}")

    schema_template = Template(SCHEMA_TEMPLATE.strip())
    schema_code = schema_template.render(
        class_name=class_name,
        columns=columns,
        need_datetime=need_datetime,
        need_date=need_date,
        need_time=need_time
    )
    output_base = table_name[len(OUTPUT_PREFIX_REMOVE):] if table_name.startswith(OUTPUT_PREFIX_REMOVE) else table_name

    output_file = os.path.join(os.getcwd(), f"{folders[4]}/{output_base}.py")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(schema_code)
    print(f"✅ schema已生成：{output_file}")


def main():
    #table_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TABLE_NAME
    engine = create_engine(DATABASE_URL)

    try:
        table_names = DEFAULT_TABLE_NAME.split(",")
        for table_name in table_names:
            generate_model_code(table_name, engine)

    except Exception as e:
        print(f"❌ 生成失败：{e}")
        raise


if __name__ == "__main__":
    main()