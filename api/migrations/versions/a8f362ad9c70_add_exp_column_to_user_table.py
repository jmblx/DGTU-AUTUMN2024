"""Add exp column to user table

Revision ID: a8f362ad9c70
Revises: a9a74f9dbadb
Create Date: 2024-10-27 13:10:41.739788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8f362ad9c70'
down_revision: Union[str, None] = 'a9a74f9dbadb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('user', sa.Column('exp', sa.Integer(), nullable=True))

def downgrade():
    op.drop_column('user', 'exp')
