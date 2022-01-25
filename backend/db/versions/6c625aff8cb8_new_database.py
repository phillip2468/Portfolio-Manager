"""New database

Revision ID: 6c625aff8cb8
Revises: ce1481a983d6
Create Date: 2022-01-22 14:30:00.466588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c625aff8cb8'
down_revision = 'ce1481a983d6'
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
    op.create_table('ticker_prices',
    sa.Column('stock_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=True),
    sa.Column('city', sa.String(length=20), nullable=True),
    sa.Column('country', sa.String(length=30), nullable=True),
    sa.Column('industry', sa.String(length=50), nullable=True),
    sa.Column('zip_code', sa.String(length=15), nullable=True),
    sa.Column('sector', sa.String(length=30), nullable=True),
    sa.Column('currency', sa.String(length=6), nullable=True),
    sa.Column('exchange', sa.String(length=10), nullable=True),
    sa.Column('stock_name', sa.String(length=150), nullable=True),
    sa.Column('market_cap', sa.BigInteger(), nullable=True),
    sa.Column('market_state', sa.String(length=20), nullable=True),
    sa.Column('quote_type', sa.String(length=10), nullable=True),
    sa.Column('market_change', sa.Float(precision=53), nullable=True),
    sa.Column('market_change_percentage', sa.Float(precision=53), nullable=True),
    sa.Column('market_high', sa.Numeric(), nullable=True),
    sa.Column('market_low', sa.Numeric(), nullable=True),
    sa.Column('market_open', sa.Numeric(), nullable=True),
    sa.Column('market_previous_close', sa.Numeric(), nullable=True),
    sa.Column('market_current_price', sa.Numeric(), nullable=True),
    sa.Column('market_volume', sa.BigInteger(), nullable=True),
    sa.Column('last_updated', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('stock_id'),
    sa.UniqueConstraint('symbol')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ticker_prices')
    op.drop_table('news_stories')
    # ### end Alembic commands ###