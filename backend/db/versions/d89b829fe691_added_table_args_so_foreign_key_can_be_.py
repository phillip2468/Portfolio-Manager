"""Added table args so foreign key can be enabled

Revision ID: d89b829fe691
Revises: c92df9890f9d
Create Date: 2022-02-03 20:47:26.671888

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'd89b829fe691'
down_revision = 'c92df9890f9d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_primary_key(
        "portfolio_composite_key",
    )


def downgrade():
    pass
