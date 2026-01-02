from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
    def get_scheduler_service(self) -> AsyncIOScheduler:
        """
        获取任务调度服务
        """
        return self.scheduler_service

    def add_job(self, **kwargs):
        self.scheduler_service.add_job(**kwargs)

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

job_scheduler = JobScheduler()