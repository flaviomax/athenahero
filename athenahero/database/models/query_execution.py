"""Data models."""
from athenahero import db
from sqlalchemy.dialects.postgresql import UUID
import uuid


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
    query = db.Column(
        db.Text,
        index=False,
        unique=False, 
        nullable=False
    )

    def __repr__(self):
        return f'<Query Execution {self.id}>'
