"""Initial migration.

Revision ID: 710c47aa760a
Revises: 
Create Date: 2022-01-04 22:11:10.799111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '710c47aa760a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ticker_prices',
    sa.Column('stock_id', sa.Integer(), nullable=False),
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
    sa.Column('last_updated', sa.DateTime(timezone=True), server_default='now()', nullable=False),
    sa.Column('symbol', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('stock_id'),
    sa.UniqueConstraint('symbol')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ticker_prices')
    # ### end Alembic commands ###