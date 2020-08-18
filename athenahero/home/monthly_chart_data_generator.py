from athenahero.database.models.query_execution import QueryExecution
from datetime import datetime, timedelta
from sqlalchemy.sql import func
from sqlalchemy import Date, desc, case
from athenahero import db 

def data_read_by_day():
    full_data = db.session.query(
        QueryExecution.submission_datetime.cast(Date).label('date'),
        func.sum(QueryExecution.data_scanned_in_bytes) / 1000000000.0
    ).filter(
        QueryExecution.submission_datetime >= datetime.today() - timedelta(days=30)
    ). group_by(
        QueryExecution.submission_datetime.cast(Date)
    ).order_by(
        'date'
    ).all()
    labels, values = zip(*full_data)
    return labels, values

def data_read_by_workgroup():
    full_data = db.session.query(
        QueryExecution.workgroup.label('workgroup'),
        (func.sum(QueryExecution.data_scanned_in_bytes) / 1000000000.0).label('total_data_scanned')
    ).filter(
        QueryExecution.submission_datetime >= datetime.today() - timedelta(days=30)
    ).group_by(
        QueryExecution.workgroup
    ).order_by(
        desc('total_data_scanned')
    ).all()
    labels, values = zip(*full_data)
    return labels, values

def get_total_read_naive_queries():
    # TODO: check semicolon impact here
    naive_categorized = db.session.query(
        case([(
                func.lag(QueryExecution.data_scanned_in_bytes).over(
                    partition_by=func.md5(QueryExecution.query_text),
                    order_by=QueryExecution.submission_datetime
                ) == QueryExecution.data_scanned_in_bytes,
                True
            )],
            else_=False
        ).label('is_naive'),
        QueryExecution.query_text,
        QueryExecution.data_scanned_in_bytes
    ).filter(
        # TODO: adjust timeframe
        QueryExecution.submission_datetime >= datetime.today() - timedelta(days=30)
    ).subquery()

    total_read_naive_queries = db.session.query(
        func.sum(naive_categorized.c.data_scanned_in_bytes) / 1000000000.0
    ).filter(
        naive_categorized.c.is_naive == True
    ).first()

    return total_read_naive_queries
