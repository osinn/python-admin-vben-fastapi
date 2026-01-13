import sched
from datetime import datetime

from core.framework.scheduler_tools import job_task


# class TaskClass:
#
#     @scheduler_manager.interval_task(
#         id="sync_job",
#         seconds=3,
#         name="监控任务"
#     )
#     async def sync_job(self):
#         # "__main__.TaskClass.sync_job"
#         now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         print(f"[同步任务] 执行时间: {now}")

# @scheduler_manager.job_task(
#     id="sync_job",
#     seconds=3,
#     name="监控任务",
#     kwargs={"x": 3}
# )
@job_task(name="cron_job任务", cron_expr="*/1 * * * *", kwargs={"x": 3})
async def sync_job(**kwargs):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[cron_job] 执行时间: {now} ====>", kwargs)

 # 在任务内部创建数据库会话
 #    with session_factory() as db:
 #        # 执行数据库操作
 #        users = db.query(User).filter(User.is_deleted == True).all()
 #        print(f"清理 {len(users)} 个已删除用户")
        # 注意：这里不能 await，因为 SQLAlchemy 同步 ORM 不支持 async/await