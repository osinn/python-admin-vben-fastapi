import importlib

from core.framework.logger import logger

async def import_modules_async(modules: list, desc: str, **kwargs):
    """
    异步动态导入模块
    :param modules:
    :param desc:
    :param kwargs:
    :return:
    """
    for module in modules:
        if not module:
            continue
        try:
            # 动态导入模块
            module_pag = importlib.import_module(module[0:module.rindex(".")])
            await getattr(module_pag, module[module.rindex(".") + 1:])(**kwargs)
        except ModuleNotFoundError:
            logger.error(f"AttributeError：导入{desc}失败，未找到该模块：{module}")
        except AttributeError:
            logger.error(f"ModuleNotFoundError：导入{desc}失败，未找到该模块下的方法：{module}")