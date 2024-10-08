"""add users table

Revision ID: b4d93add66ef
Revises: 542d1dbcef6a
Create Date: 2020-07-08 16:18:18.869524

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b4d93add66ef'
down_revision = '542d1dbcef6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('tags')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tags', mysql.TEXT(), nullable=True))

    # ### end Alembic commands ###
