"""Made some fields not nullable

Revision ID: 328b0961374b
Revises: eaabfc3e14a5
Create Date: 2022-02-08 16:33:27.166357

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '328b0961374b'
down_revision = 'eaabfc3e14a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('user', 'hashed_password',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('user', 'last_signed_in',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False,
               existing_server_default=sa.text('now()'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'last_signed_in',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True,
               existing_server_default=sa.text('now()'))
    op.alter_column('user', 'hashed_password',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('user', 'email',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###