import os
from typing import Optional

import ip2region.util as util
import ip2region.searcher as xdb
from core.framework.log_tools import logger, BASE_DIR


class IpLocationService:
    def __init__(self):
        print("ip2region_v4 初始化")
        # 获取项目根目录
        db_path = os.path.join(BASE_DIR, "lib", "ip2region_v4.xdb")

        # 检查文件是否存在
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"IP数据库文件不存在: {db_path}")

        c_buffer = util.load_content_from_file(db_path)
        version = util.IPv4
        self.searcher = xdb.new_with_buffer(version, c_buffer)

    def get_ip_address_attr(self, ip) -> Optional[str]:
        try:
            region = self.searcher.search(ip)
            if "内网IP" in region:
                _, _, ip_address_attr, _ = region.split('|')
                return ip_address_attr
            else:
                return region
        except Exception as e:
            logger.error(f"ip地址归属地搜索异常: {str(e)}")
            return None

    def close(self):
        print("ip2region_v4 关闭资源")
        self.searcher.close()

ip_location_service = IpLocationService()
