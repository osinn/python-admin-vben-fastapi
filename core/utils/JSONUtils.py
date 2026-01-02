import json
import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Union
from pathlib import Path


class JSONUtils:
    """JSON工具类"""

    @staticmethod
    def dumps(obj: Any, **kwargs) -> str:
        """
        将Python对象转换为JSON字符串

        Args:
            obj: 要序列化的Python对象
            **kwargs: 传递给json.dumps的其他参数

        Returns:
            JSON字符串
        """
        default_kwargs = {
            'ensure_ascii': False,
            'indent': 2,
            'sort_keys': True
        }
        default_kwargs.update(kwargs)

        return json.dumps(obj, default=JSONUtils._default_encoder, **default_kwargs)

    @staticmethod
    def loads(json_str: str, **kwargs) -> Any:
        """
        将JSON字符串转换为Python对象

        Args:
            json_str: JSON字符串
            **kwargs: 传递给json.loads的其他参数

        Returns:
            Python对象
        """
        return json.loads(json_str, **kwargs)

    @staticmethod
    def _default_encoder(obj: Any) -> Any:
        """
        自定义JSON序列化器，处理特殊类型

        Args:
            obj: 要序列化的对象

        Returns:
            可序列化的对象
        """
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, bytes):
            return obj.decode('utf-8', errors='ignore')
        elif hasattr(obj, '__dict__'):
            # 处理自定义对象
            return obj.__dict__
        elif hasattr(obj, '_asdict'):
            # 处理namedtuple
            return obj._asdict()

        raise TypeError(f'Object of type {type(obj)} is not JSON serializable')

    @staticmethod
    def pretty_print(obj: Any) -> None:
        """
        美化打印JSON对象

        Args:
            obj: Python对象
        """
        formatted_json = JSONUtils.dumps(obj, indent=2, ensure_ascii=False)
        print(formatted_json)

    @staticmethod
    def to_file(obj: Any, file_path: Union[str, Path], **kwargs) -> bool:
        """
        将Python对象保存到JSON文件

        Args:
            obj: Python对象
            file_path: 文件路径
            **kwargs: 传递给dumps的参数

        Returns:
            是否成功
        """
        try:
            file_path = Path(file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            json_str = JSONUtils.dumps(obj, **kwargs)
            file_path.write_text(json_str, encoding='utf-8')
            return True
        except Exception as e:
            print(f"保存JSON文件失败: {e}")
            return False

    @staticmethod
    def from_file(file_path: Union[str, Path], **kwargs) -> Any:
        """
        从JSON文件读取Python对象

        Args:
            file_path: 文件路径
            **kwargs: 传递给loads的参数

        Returns:
            Python对象或None
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None

            json_str = file_path.read_text(encoding='utf-8')
            return JSONUtils.loads(json_str, **kwargs)
        except Exception as e:
            print(f"读取JSON文件失败: {e}")
            return None

    @staticmethod
    def is_valid_json(json_str: str) -> bool:
        """
        检查字符串是否为有效的JSON

        Args:
            json_str: JSON字符串

        Returns:
            是否为有效JSON
        """
        try:
            JSONUtils.loads(json_str)
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    @staticmethod
    def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
        """
        深度合并两个字典

        Args:
            dict1: 第一个字典
            dict2: 第二个字典

        Returns:
            合并后的字典
        """
        result = dict1.copy()

        for key, value in dict2.items():
            if (key in result and
                    isinstance(result[key], dict) and
                    isinstance(value, dict)):
                result[key] = JSONUtils.deep_merge(result[key], value)
            else:
                result[key] = value

        return result