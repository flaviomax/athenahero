"""create query_text md5 hash

Revision ID: c53f4d70de26
Revises: 68667e0da916
Create Date: 2020-08-18 07:34:53.077349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c53f4d70de26'
down_revision = '68667e0da916'
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
