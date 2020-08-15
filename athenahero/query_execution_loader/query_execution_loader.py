import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from flask import current_app
from . import query_execution_loader_job

if current_app.config['ENV'] == 'production':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=query_execution_loader_job.save_execution_to_file, trigger="interval", minutes=1)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
