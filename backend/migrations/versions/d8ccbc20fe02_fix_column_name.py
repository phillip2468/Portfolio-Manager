"""fix column name

Revision ID: d8ccbc20fe02
Revises: 75627abbd454
Create Date: 2022-01-06 21:03:11.547829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8ccbc20fe02'
down_revision = '75627abbd454'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ticker_prices', sa.Column('market_volume', sa.BigInteger(), nullable=True))
    op.drop_column('ticker_prices', 'market_volume_1')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ticker_prices', sa.Column('market_volume_1', sa.BIGINT(), autoincrement=False, nullable=True))
    op.drop_column('ticker_prices', 'market_volume')
    # ### end Alembic commands ###