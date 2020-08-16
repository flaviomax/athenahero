from athenahero.database.models.query_execution import QueryExecution
from datetime import datetime, timedelta
from sqlalchemy.sql import func
from sqlalchemy import Date
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
