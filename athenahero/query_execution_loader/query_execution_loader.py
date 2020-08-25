import atexit
import time
from datetime import datetime, timedelta

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app

from . import query_execution_loader_job


def register_query_execution_job():
    if current_app.config['ENV'] == 'production':
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            name='last_30_days_updater',
            id='last_30_days_updater',
            func=query_execution_loader_job.populate_month_of_executions,
            trigger="interval",
            hours=6,
            coalesce=True,
            max_instances=1,
            next_run_time=datetime.now() + timedelta(seconds=3),
            misfire_grace_time=30
        )
        scheduler.start()

        # Shut down the scheduler when exiting the app
        atexit.register(lambda: scheduler.shutdown())
