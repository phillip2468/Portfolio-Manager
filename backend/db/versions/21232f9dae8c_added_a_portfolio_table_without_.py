"""Added a portfolio table without constraints

Revision ID: 21232f9dae8c
Revises: c3f87ae36c53
Create Date: 2022-02-03 19:23:39.198031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21232f9dae8c'
down_revision = 'c3f87ae36c53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news_stories',
    sa.Column('story_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('short_description', sa.Text(), nullable=True),
    sa.Column('url', sa.Text(), nullable=True),
    sa.Column('image_url', sa.Text(), nullable=True),
    sa.Column('article_updated', sa.Text(), nullable=True),
    sa.Column('last_updated', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('story_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news_stories')
    # ### end Alembic commands ###