"""Changed the requirements of the jwt package, so the table must be modified

Revision ID: e67bdb995317
Revises: 7ada145faadc
Create Date: 2022-01-27 14:01:42.738489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e67bdb995317'
down_revision = '7ada145faadc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'roles')
    op.drop_column('user', 'is_active')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_active', sa.BOOLEAN(), server_default=sa.text('true'), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('roles', sa.TEXT(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
