"""create md5 index on query_text on query_executions

Revision ID: 451bc477cfa6
Revises: 9665fcbf9b01
Create Date: 2020-08-24 20:50:55.846047

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '451bc477cfa6'
down_revision = '9665fcbf9b01'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """ CREATE INDEX query_executions_query_text_md5_index
            ON query_executions
            (MD5(query_text))
        """
    )


def downgrade():
    op.execute("DROP INDEX query_executions_query_text_md5_index")
