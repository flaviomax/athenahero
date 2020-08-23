TESTING = True
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/athenahero'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JOBS = [
#         {
#             'id': 'last_30_days_update_immediately',
#             'func': '.query_execution_loader.query_execution_loader_job:populate_month_of_executions',
#             # 'trigger': 'interval',
#             # 'hours': 6
#         }
#     ]

# SCHEDULER_JOBSTORES = {
#     'default': SQLAlchemyJobStore(url='sqlite://')
# }

# SCHEDULER_EXECUTORS = {
#     'default': {'type': 'threadpool', 'max_workers': 20}
# }

SCHEDULER_JOB_DEFAULTS = {
    'coalesce': True,
    'max_instances': 1
}

SCHEDULER_API_ENABLED = True
