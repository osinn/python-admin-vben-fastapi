from typing import Optional, Dict, Any
from user_agents import parse
import ip2region.searcher as xdb

class WebRequestUtils:
    """Web请求工具类：封装获取客户端IP、浏览器信息等功能"""

    @staticmethod
    def get_client_ip(request: Any) -> str:
        """
        获取客户端真实IP地址
        :param request: 框架的请求对象（FastAPI/Flask/Django的request）
        :return: 客户端IP字符串，获取失败返回空字符串
        """
        try:
            # 1. 优先解析代理传递的真实IP头（X-Forwarded-For）
            # 适配不同框架的请求头获取方式
            if hasattr(request, 'headers'):
                # FastAPI/Flask
                x_forwarded_for = request.headers.get("X-Forwarded-For", "")
                x_real_ip = request.headers.get("X-Real-IP", "")
            elif hasattr(request, 'META'):
                # Django
                x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
                x_real_ip = request.META.get("HTTP_X_REAL_IP", "")
            else:
                x_forwarded_for = ""
                x_real_ip = ""

            # 解析X-Forwarded-For（格式：client_ip, proxy1, proxy2...）
            if x_forwarded_for:
                ip = x_forwarded_for.split(",")[0].strip()
                if ip and ip != "unknown":
                    return ip

            # 解析X-Real-IP
            if x_real_ip:
                ip = x_real_ip.strip()
                if ip and ip != "unknown":
                    return ip

            # 2. 获取原生客户端IP（适配不同框架）
            if hasattr(request, 'client') and request.client:
                # FastAPI
                ip = request.client.host
            elif hasattr(request, 'remote_addr'):
                # Flask
                ip = request.remote_addr
            elif hasattr(request, 'META'):
                # Django
                ip = request.META.get("REMOTE_ADDR", "")
            else:
                ip = ""

            # 处理IPv6格式（去除端口，如 [::1]:54321 → ::1）
            if ip and ":" in ip and "[" not in ip:
                ip = ip.split(":")[0]

            return ip.strip() if ip else ""

        except Exception as e:
            # 异常时返回空字符串，避免程序崩溃
            print(f"获取客户端IP失败：{str(e)}")
            return ""

    @staticmethod
    def get_browser_info(request: Any) -> Dict[str, Optional[str]]:
        """
        获取客户端浏览器信息
        :param request: 框架的请求对象（FastAPI/Flask/Django的request）
        :return: 包含浏览器名称、版本、系统等信息的字典
        """
        try:
            # 1. 获取User-Agent字符串
            if hasattr(request, 'headers'):
                user_agent_str = request.headers.get("User-Agent", "")  # FastAPI/Flask
            elif hasattr(request, 'META'):
                user_agent_str = request.META.get("HTTP_USER_AGENT", "")  # Django
            else:
                user_agent_str = ""

            if not user_agent_str:
                return {
                    "browser_name": None,
                    "browser_version": None,
                    "os_name": None,
                    "os_version": None,
                    "is_mobile": False,
                    "device_type": None
                }

            # 2. 解析User-Agent
            user_agent = parse(user_agent_str)

            # 3. 封装返回结果
            return {
                "browser_name": user_agent.browser.family,  # 浏览器名称（Chrome/Firefox等）
                "browser_version": user_agent.browser.version_string,  # 浏览器版本
                "os_name": user_agent.os.family,  # 操作系统名称
                "os_version": user_agent.os.version_string,  # 系统版本
                "is_mobile": user_agent.is_mobile,  # 是否移动端
                "device_type": user_agent.device.family  # 设备类型（iPhone/Windows等）
            }

        except Exception as e:
            print(f"获取浏览器信息失败：{str(e)}")
            return {
                "browser_name": None,
                "browser_version": None,
                "os_name": None,
                "os_version": None,
                "is_mobile": False,
                "device_type": None
            }

    @staticmethod
    def get_request_info(request: Any) -> Dict[str, Any]:
        """
        一次性获取所有客户端请求信息（IP+浏览器）
        :param request: 框架的请求对象
        :return: 整合后的请求信息字典
        """
        return {
            "client_ip": WebRequestUtils.get_client_ip(request),
            "browser_info": WebRequestUtils.get_browser_info(request)
        }

    @staticmethod
    def get_ip_address_attr():
        pass
        # # 1，使用上述的 version 和 db_path 创建完全基于文件的查询对象
        # try:
        #     searcher = xdb.new_with_file_only(version, db_path)
        # except Exception as e:
        #     print(f"failed to new_with_file_only: {str(e)}")
        #     return
        #
        # # 2、查询，IPv4 或者 IPv6 的地址都是同一个接口
        # ip = "1.2.3.4"
        # # ip = "240e:3b7:3272:d8d0:db09:c067:8d59:539e"  // IPv6
        # try:
        #     region = searcher.search(ip)
        #     print(f"search({ip}): {{region: {region}, io_count: {searcher.get_io_count()}}}")
        # except Exception as e:
        #     print(f"failed to search: {str(e)}")
        #
        # # 3、关闭资源
        # searcher.close()
