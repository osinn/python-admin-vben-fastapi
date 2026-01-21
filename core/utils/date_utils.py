import datetime
from typing import Union, Optional


def format_timestamp(timestamp: Union[int, float],
                     fmt: str = "%Y-%m-%d %H:%M:%S",
                     timezone: str = 'local') -> Optional[str]:
    """
    格式化时间戳

    Args:
        timestamp: 秒级时间戳
        fmt: 格式字符串，默认为 "%Y-%m-%d %H:%M:%S"
        timezone: 时区，'local' 或 'utc'

    Returns:
        格式化后的时间字符串
    """
    if timestamp is None:
        return None
    try:
        if timezone.lower() == 'utc':
            dt = datetime.datetime.fromtimestamp(timestamp, datetime.UTC)
        else:
            dt = datetime.datetime.fromtimestamp(timestamp)

        return dt.strftime(fmt)
    except (ValueError, OSError) as e:
        raise ValueError(f"无效的时间戳: {timestamp}") from e