from datetime import datetime, timedelta

from sqlalchemy import Date, case, desc
from sqlalchemy.sql import func

from athenahero import db
from athenahero.database.models.query_execution import QueryExecution


def data_read_by_day():
    full_data = (
        db.session.query(
            QueryExecution.submission_datetime.cast(Date).label("date"),
            func.sum(QueryExecution.data_scanned_in_bytes) / 1000000000.0,
        )
        .filter(QueryExecution.submission_datetime >= datetime.today() - timedelta(days=30))
        .group_by(QueryExecution.submission_datetime.cast(Date))
        .order_by("date")
        .all()
    )
    if full_data:
        labels, values = zip(*full_data)
    else:
        labels, values = [], []
    return labels, values


def data_read_by_workgroup():
    full_data = (
        db.session.query(
            QueryExecution.workgroup.label("workgroup"),
            (func.sum(QueryExecution.data_scanned_in_bytes) / 1000000000.0).label("total_data_scanned"),
        )
        .filter(QueryExecution.submission_datetime >= datetime.today() - timedelta(days=30))
        .group_by(QueryExecution.workgroup)
        .order_by(desc("total_data_scanned"))
        .all()
    )
    if full_data:
        labels, values = zip(*full_data)
    else:
        labels, values = [], []
    return labels, values


def get_queries_data():
    # TODO: check semicolon impact here
    most_expensive_queries = (
        db.session.query(
            QueryExecution.query_text,
            func.count(QueryExecution.query_text).label("query_count"),
            (func.avg(QueryExecution.data_scanned_in_bytes) / 1000000000.0).label("avg_gb_read"),
            (func.sum(QueryExecution.data_scanned_in_bytes) / 1000000000.0).label("total_gb_read"),
        )
        .filter(QueryExecution.submission_datetime >= datetime.today() - timedelta(days=30))
        .group_by(func.md5(QueryExecution.query_text), QueryExecution.query_text)
        .order_by(desc("total_gb_read"))
        .limit(10)
        .all()
    )

    return most_expensive_queries


def get_naive_queries_data():
    # TODO: check semicolon impact here
    naive_categorized = (
        db.session.query(
            case(
                [
                    (
                        func.lag(QueryExecution.data_scanned_in_bytes).over(
                            partition_by=func.md5(QueryExecution.query_text),
                            order_by=QueryExecution.submission_datetime,
                        )
                        == QueryExecution.data_scanned_in_bytes,
                        True,
                    )
                ],
                else_=False,
            ).label("is_naive"),
            QueryExecution.query_text,
            QueryExecution.data_scanned_in_bytes,
        )
        .filter(QueryExecution.submission_datetime >= datetime.today() - timedelta(days=30))
        .subquery()
    )

    total_bytes_read = (
        db.session.query(func.sum(naive_categorized.c.data_scanned_in_bytes) / 1000000000.0)
        .filter(naive_categorized.c.is_naive == True)
        .first()
    )

    # we are assuming no hash collisions here
    most_expensive_naive_queries = (
        db.session.query(
            naive_categorized.c.query_text,
            func.count(naive_categorized.c.query_text).label("query_count"),
            (func.avg(naive_categorized.c.data_scanned_in_bytes) / 1000000000.0).label("avg_gb_read"),
            (func.sum(naive_categorized.c.data_scanned_in_bytes) / 1000000000.0).label("total_gb_read"),
        )
        .filter(naive_categorized.c.is_naive == True)
        .group_by(func.md5(naive_categorized.c.query_text), naive_categorized.c.query_text)
        .order_by(desc("total_gb_read"))
        .limit(10)
        .all()
    )

    return {"total_bytes_read": total_bytes_read, "most_expensive_queries": most_expensive_naive_queries}
