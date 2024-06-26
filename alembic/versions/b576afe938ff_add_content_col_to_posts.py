"""add content col to posts

Revision ID: b576afe938ff
Revises: c480ff5510d3
Create Date: 2024-06-25 15:13:59.162271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b576afe938ff'
down_revision: Union[str, None] = 'c480ff5510d3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_column('posts','content')
