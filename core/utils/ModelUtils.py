from datetime import datetime, date
from typing import Any


class ModelUtils:
    """Django模型工具类"""

    # @staticmethod
    # def to_dict(instance, exclude_attrs=None):
    #     """
    #     将模型实例转换为字典，排除内部属性
    #     示例：user_dict = ModelUtils.to_dict(user)
    #
    #     Args:
    #         instance: 模型实例
    #         exclude_attrs: 要排除的属性列表
    #     Returns:
    #         dict: 返回转换好的字典
    #     """
    #     if exclude_attrs is None:
    #         exclude_attrs = ['_state', '_django_version']

    #     # 判断实例是否不为空且是否包含 __dict__
    #     if instance is not None and hasattr(instance, '__dict__'):
    #         return {
    #             key: value
    #             for key, value in instance.__dict__.items()
    #             if key not in exclude_attrs
    #         }
    #     else:
    #         return instance

    @staticmethod
    def to_dict(obj: Any, exclude_attrs=None) -> Any:
        """
        对象转换字典
        :param obj: 任意数据（字典/列表/Pydantic模型/ORM对象等）
        :param exclude_attrs: 要排除的属性列表
        :return: 格式化后的数据（datetime 转为字符串）
        """
        if exclude_attrs is None:
            exclude_attrs = ['_state', '_django_version']

        # 1. 处理 datetime 类型（核心：格式化时间）
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        # 2. 处理列表/元组（递归遍历元素）
        elif isinstance(obj, (list, tuple)):
            return [ModelUtils.to_dict(item) for item in obj]
        # 3. 处理字典（递归遍历键值对）
        elif isinstance(obj, dict):
            return {key: ModelUtils.to_dict(value) for key, value in obj.items() if key not in exclude_attrs}
        # 4. 兼容 Pydantic v2 模型（自动转字典后格式化）
        elif hasattr(obj, "model_dump"):
            return ModelUtils.to_dict(obj.model_dump())
        # 5. 兼容 Pydantic v1 模型（兼容旧版本）
        elif hasattr(obj, "dict"):
            return ModelUtils.to_dict(obj.dict())
        # 6. 兼容 ORM/自定义对象（需实现 to_dict 方法）
        elif hasattr(obj, "to_dict"):
            return ModelUtils.to_dict(obj.to_dict())
        # 7. 其他类型（int/str/bool/None 等）原样返回
        else:
            return obj

    @staticmethod
    def dict_instance_attr(data_dict, instance, exclude_attrs=None):
        """
        从字典更新模型实例属性
        示例
            # 准备更新数据
            update_data = {
                'user_name': '新的用户名',
                'user_email': 'new@example.com',
            }

            # 使用 dict_instance_attr 更新对象
            ModelUtils.dict_instance_attr(user, update_data)
        Args:
            instance: 模型实例
            data_dict: 数据字典
            exclude_attrs: 要排除的属性列表
        """
        if exclude_attrs is None:
            exclude_attrs = ['_state', '_django_version']

        for key, value in data_dict.items():
            if (key not in exclude_attrs and
                    hasattr(instance, key) and
                    not key.startswith('_')):
                setattr(instance, key, value)

    @staticmethod
    def copy_attributes(source, target, exclude_attrs=None):
        """
        复制源对象的属性到目标对象

        Args:
            target: 目标对象
            source: 源对象
            exclude_attrs: 要排除的属性列表
        """
        if exclude_attrs is None:
            exclude_attrs = ['_state', '_django_version', 'pk']
            # exclude_attrs = ['_state', '_django_version', 'id', 'pk']

        source_dict = ModelUtils.to_dict(source, exclude_attrs)
        ModelUtils.dict_instance_attr(source_dict, target, exclude_attrs)
