import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from . import query_execution_loader_job

def register_query_execution_job():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        name='last_30_days_updater',
        func=query_execution_loader_job.populate_month_of_executions,
        trigger="interval",
        hours=6,
        coalesce=True,
        max_instances=1
        )
    scheduler.add_job(
        name='last_30_days_update_immediately',
        func=query_execution_loader_job.populate_month_of_executions,
        coalesce=True
    )
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown(wait=False))
