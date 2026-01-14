import importlib
import sys
import time

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.ext.asyncio import AsyncSession

from apps.modules.sys.scheduler.models.job_scheduler import JobSchedulerModel
from core.framework.log_tools import logger
from core.framework.sql_alchemy_helper import SQLAlchemyHelper
from core.utils.JSONUtils import JSONUtils


class JobScheduler:

    """调度器单例"""
    _instance = None
    scheduler_service = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init_scheduler(self, db_url: str = None):
        """
        初始化任务调度
        """
        """初始化"""
        jobstores = {
            # 使用mysql 存储调度信息，存储表启动后会自动创建，如果不指定表名 会自动创建apscheduler_jobs表，
            # 使用 asyncmy 会报错
            'default': SQLAlchemyJobStore(url=db_url
                                          # , tablename='my_task'
                                          )
            # SQLAlchemyJobStore指定存储链接
        }
        # global scheduler # 全局变量

        scheduler = AsyncIOScheduler()
        scheduler.configure(jobstores=jobstores)

        self.scheduler_service = scheduler

        self.scheduler_service.start()
        # scheduler_manager.register_all_tasks()

    def get_scheduler_service(self) -> AsyncIOScheduler:
        """
        获取任务调度服务
        """
        return self.scheduler_service

    def add_job(self, **kwargs):
        self.scheduler_service.add_job(**kwargs)

    def remove_job(self, job_id, jobstore=None):
        self.scheduler_service.remove_job(job_id=job_id, jobstore=jobstore)

    def start(self):
        """
        启动调度服务
        """
        self.scheduler_service.start()

    def shutdown(self):
        """
        关闭调度
        """
        self.scheduler_service.shutdown()

    def add_job_from_config(self, job_param):
        """从配置字典添加任务"""
        job_id = job_param.get("id")

        if not job_id:
            raise ValueError("任务配置必须包含id字段")

        # 保存配置
        # self.job_configs[job_id] = job_param

        # 动态导入函数
        func = self._import_function(job_param.get("func"))

        # 构建参数
        trigger_type = job_param.get("trigger", "interval")

        # 移除不需要的参数
        param_copy = job_param.copy()
        for key in ["func", "trigger", "id"]:
            param_copy.pop(key, None)

        # 添加任务
        job = self.scheduler_service.add_job(
            func=func,
            trigger=trigger_type,
            id=job_id,
            **param_copy
        )

        print(f"已添加任务: {job_id}")
        return job

    def _import_function(self, func_path):
        """导入函数（支持多种格式）"""
        if not func_path:
            raise ValueError("func参数不能为空")

        # 尝试不同的导入方式
        if '.' not in func_path:
            # 尝试从当前模块导入
            caller_frame = sys._getframe(2)
            caller_module = caller_frame.f_globals['__name__']
            module = importlib.import_module(caller_module)
            if hasattr(module, func_path):
                return getattr(module, func_path)

        # 尝试从指定路径导入
        parts = func_path.rsplit('.', 1)
        if len(parts) == 2:
            module_name, function_name = parts
            try:
                module = importlib.import_module(module_name)
                return getattr(module, function_name)
            except ImportError:
                pass

        raise ValueError(f"无法导入函数: {func_path}")

class SchedulerManager:
    def __init__(self):
        self.tasks = {}

    def job_task(
        self,
        # Interval 参数
        seconds=None,
        minutes=0,
        hours=0,
        # Cron 表达式（字符串）
        cron_expr: str = None,   # ← 新增：支持 "*/5 * * * *" 等
        # 原 cron 字典参数（可选保留）
        cron: dict = None,
        name=None,
        remarks: str = "",
        author: str = "Default author",
        alarm_email: str = "",
        is_run: bool = True,
        kwargs: dict = None,
    ):
        def decorator(func):
            module = func.__module__
            func_name = func.__name__
            full_path = f"{module}.{func_name}"
            task_id = full_path

            # 判断触发器类型
            if cron_expr is not None:
                # 使用 cron 表达式字符串
                trigger_type = "cron"
                job_trigger_type = 3
                trigger_args = {"cron_expr": cron_expr}
            elif cron is not None:
                trigger_type = "cron"
                trigger_args = cron
                job_trigger_type = 3
            else:
                trigger_type = "interval"
                job_trigger_type = 2
                trigger_args = {}
                if seconds is not None:
                    trigger_args["seconds"] = seconds
                if minutes:
                    trigger_args["minutes"] = minutes
                if hours:
                    trigger_args["hours"] = hours
                if not trigger_args:
                    raise ValueError("必须指定时间参数")

                # 创建结果字典
            extra_kwarg = {
                "job_id": task_id,
                "trigger_type": job_trigger_type,
                "trigger_condition":JSONUtils.dumps(trigger_args),
                "remarks": remarks,
                "author": author,
                "alarm_email": alarm_email,
                "executor_param": kwargs,
                "executor_handler": func_name
            }
            task_info = self.tasks.get(task_id, None)
            if task_info is not None:
                logger.error(f"【{task_id}】任务ID不能重复，程序已退出运行")
                time.sleep(1)
                exit(0)
            self.tasks[task_id] = {
                "func": func,
                "full_path": full_path,
                "is_run": is_run,
                "trigger_type": trigger_type,
                "trigger_args": trigger_args,
                "name": name or func_name,
                "id": task_id,
                "kwargs": extra_kwarg,
            }
            return func

        return decorator

    async def register_all_tasks(self, db: AsyncSession):
        """
        注册所有被装饰的任务
        """
        scheduler_service = job_scheduler.get_scheduler_service()
        job_all = scheduler_service.get_jobs()
        job_ids = [job_info.id for job_info in job_all]
        for task_id, task_info in self.tasks.items():
            if task_id in job_ids:
                scheduler_service.remove_job(task_info['id'])
            job_scheduler_model: JobSchedulerModel = await SQLAlchemyHelper.get_by_key(db, "job_id", task_id, JobSchedulerModel)

            # 保存报错，未解决
            kwargs = task_info["kwargs"]
            if job_scheduler_model is None:
                job_scheduler_model = JobSchedulerModel()
                job_scheduler_model.created_by = -1
            job_scheduler_model.job_id = kwargs["job_id"]
            job_scheduler_model.trigger_type = kwargs["trigger_type"]
            job_scheduler_model.trigger_condition = kwargs["trigger_condition"]
            job_scheduler_model.remarks = kwargs["remarks"]
            job_scheduler_model.author = kwargs["author"]
            job_scheduler_model.alarm_email = kwargs["alarm_email"]
            job_scheduler_model.executor_param = kwargs["executor_param"]
            job_scheduler_model.executor_handler = kwargs["executor_handler"]

            if isinstance(job_scheduler_model.executor_param, dict):
                job_scheduler_model.executor_param = JSONUtils.dumps(job_scheduler_model.executor_param)

            if job_scheduler_model.id is None:
                db.add(job_scheduler_model)
            await db.flush()

            if task_info["is_run"] == False:
                continue

            trigger_type = task_info["trigger_type"]
            trigger_args = task_info["trigger_args"]
            if trigger_type == "cron":
                if "cron_expr" in trigger_args:
                    # 解析 cron 表达式字符串
                    cron_expr = trigger_args["cron_expr"]
                    """表达式字符串（5 位）
                      * * * * * <command to execute>
                    # | | | | |
                    # | | | | day of the week (0–6) (Sunday to Saturday; 
                    # | | | month (1–12)             7 is also Sunday on some systems)
                    # | | day of the month (1–31)
                    # | hour (0–23)
                    # minute (0–59)
                    最终
                    minute=values[0],
                    hour=values[1],
                    day=values[2],
                    month=values[3],
                    day_of_week=values[4],
                    timezone=timezone,
                    """
                    trigger = CronTrigger.from_crontab(cron_expr)
                    scheduler_service.add_job(
                        func=task_info["func"],
                        trigger=trigger,  # ← 传入 Trigger 实例
                        id=task_info["id"],
                        name=task_info["name"],
                        kwargs=task_info["kwargs"],
                        replace_existing=True,
                    )
                else:
                    # 原来的 cron 字典方式
                    scheduler_service.add_job(
                        func=task_info["func"],
                        trigger="cron",
                        **trigger_args,
                        id=task_info["id"],
                        name=task_info["name"],
                        kwargs=task_info["kwargs"],
                        replace_existing=True,
                    )
            else:  # interval
                scheduler_service.add_job(
                    func=task_info["func"],
                    trigger="interval",
                    **trigger_args,
                    id=task_info["id"],
                    name=task_info["name"],
                    kwargs=task_info["kwargs"],
                    replace_existing=True,
                )
        print(f"注册任务调度完成")
        await db.commit()

# 创建全局调度器管理器
scheduler_manager = SchedulerManager()
job_task = scheduler_manager.job_task

job_scheduler = JobScheduler()
