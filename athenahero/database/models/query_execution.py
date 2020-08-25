"""Data models."""
import uuid

from sqlalchemy import Index, func
from sqlalchemy.dialects.postgresql import UUID

from athenahero import db


class QueryExecution(db.Model):
    """Data model for Query Executions."""

    __tablename__ = 'query_executions'
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
    )
    query_text = db.Column(
        db.Text,
        index=False,
        unique=False, 
        nullable=False
    )
    statement_type = db.Column(
        db.String(10),
        index=False,
        unique=False, 
        nullable=False
    )
    output_location = db.Column(
        db.Text,
        index=False,
        unique=False, 
        nullable=False
    )
    encryption_option = db.Column(
        db.String(10),
        index=False,
        unique=False, 
        nullable=True
    )
    kms_key = db.Column(
        db.Text,
        index=False,
        unique=False, 
        nullable=True
    )
    context_database = db.Column(
        db.Text,
        index=False,
        unique=False, 
        nullable=True
    )
    context_catalog = db.Column(
        db.Text,
        index=False,
        unique=False, 
        nullable=True
    )
    status = db.Column(
        db.String(10),
        index=False,
        unique=False, 
        nullable=False
    )
    last_state_change_reason = db.Column(
        db.Text,
        index=False,
        unique=False, 
        nullable=True
    )
    submission_datetime = db.Column(
        db.TIMESTAMP,
        index=True,
        unique=False, 
        nullable=False
    )
    completion_datetime = db.Column(
        db.TIMESTAMP,
        index=False,
        unique=False, 
        nullable=False
    )
    engine_execution_time_in_millis = db.Column(
        db.Integer,
        index=False,
        unique=False, 
        nullable=True
    )
    total_execution_time_in_millis = db.Column(
        db.Integer,
        index=False,
        unique=False, 
        nullable=False
    )
    query_queue_time_in_millis = db.Column(
        db.Integer,
        index=False,
        unique=False, 
        nullable=True
    )
    query_planning_time_in_millis = db.Column(
        db.Integer,
        index=False,
        unique=False, 
        nullable=True
    )
    service_processing_time_in_millis = db.Column(
        db.Integer,
        index=False,
        unique=False, 
        nullable=True
    )
    data_manifest_location = db.Column(
        db.Text,
        index=False,
        unique=False, 
        nullable=True
    )
    data_scanned_in_bytes = db.Column(
        db.BigInteger,
        index=False,
        unique=False, 
        nullable=False
    )
    # TODO: change nullable to False
    workgroup  = db.Column(
        db.Text,
        index=False,
        unique=False, 
        nullable=False
    )

    def __repr__(self):
        return f'<Query Execution {self.id}>'

# TODO: do not forget to manually add this migration on first deploy
# read https://stackoverflow.com/questions/42153301/flask-sqlalchemy-lower-case-index-skipping-functional-not-supported-by-sqlalc
Index('query_executions_query_text_md5_index', func.md5(QueryExecution.query_text))
