"""add contact number to my posts table

Revision ID: 998d965ecbf0
Revises: 4196e761493f
Create Date: 2025-11-04 01:33:25.648551

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision: str = '998d965ecbf0'
down_revision: Union[str, Sequence[str], None] = '4196e761493f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add phone_number column to posts table."""
    op.add_column('posts', Column('phone_number', String(), nullable=True))


def downgrade() -> None:
    """Remove phone_number column (rollback)."""
    op.drop_column('posts', 'phone_number')