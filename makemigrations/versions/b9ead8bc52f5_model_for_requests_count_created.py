"""model for requests count created

Revision ID: b9ead8bc52f5
Revises: b8897d8f2b8a
Create Date: 2024-05-28 11:45:42.848196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9ead8bc52f5'
down_revision: Union[str, None] = 'b8897d8f2b8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request_counts', sa.Column('banned_time', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('request_counts', 'banned_time')
    # ### end Alembic commands ###
