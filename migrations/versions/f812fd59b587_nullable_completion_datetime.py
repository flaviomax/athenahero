"""nullable completion datetime

Revision ID: f812fd59b587
Revises: 451bc477cfa6
Create Date: 2020-09-25 18:49:30.060814

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f812fd59b587'
down_revision = '451bc477cfa6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('query_executions', 'completion_datetime',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.create_unique_constraint(None, 'query_executions', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'query_executions', type_='unique')
    op.alter_column('query_executions', 'completion_datetime',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###
