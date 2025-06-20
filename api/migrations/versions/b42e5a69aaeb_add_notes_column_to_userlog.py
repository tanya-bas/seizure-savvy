"""Add notes column to UserLog

Revision ID: b42e5a69aaeb
Revises: 034925cf9084
Create Date: 2024-04-19 12:48:44.478736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b42e5a69aaeb'
down_revision = '034925cf9084'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_logs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('note', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_logs', schema=None) as batch_op:
        batch_op.drop_column('note')

    # ### end Alembic commands ###
