"""add users table

Revision ID: 542d1dbcef6a
Revises: f2ebe91f3c79
Create Date: 2020-07-08 15:25:17.423026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '542d1dbcef6a'
down_revision = 'f2ebe91f3c79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts_tags',
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_posts_tags_post_id_posts')),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], name=op.f('fk_posts_tags_tag_id_tags'))
    )
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tags', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('tags')

    op.drop_table('posts_tags')
    # ### end Alembic commands ###
