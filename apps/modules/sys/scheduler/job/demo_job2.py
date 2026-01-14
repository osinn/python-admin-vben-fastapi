import sched
from datetime import datetime

from core.framework.scheduler_tools import job_task

@job_task(
    seconds=3,
    name="interval_job任务",
    kwargs={"x": 3},
    is_run=False
)
async def sync_job(**kwargs):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[interval_job] 执行时间: {now} ====>", kwargs)
