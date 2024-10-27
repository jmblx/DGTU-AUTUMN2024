"""empty message

Revision ID: 4cebeea6f9ff
Revises: 9af706d072e6
Create Date: 2024-10-27 05:12:40.196775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cebeea6f9ff'
down_revision: Union[str, None] = '9af706d072e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('achievement', sa.Column('goal', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('achievement', 'goal')
    # ### end Alembic commands ###