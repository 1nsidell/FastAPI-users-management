"""nickname unique fix

Revision ID: 168a6e9e8620
Revises: 38d83670f4ba
Create Date: 2025-02-28 19:46:01.973576

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "168a6e9e8620"
down_revision: Union[str, None] = "38d83670f4ba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "info_users", "role_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.drop_index("ix_info_users_nickname", table_name="info_users")
    op.create_index(
        op.f("ix_info_users_nickname"), "info_users", ["nickname"], unique=True
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_info_users_nickname"), table_name="info_users")
    op.create_index(
        "ix_info_users_nickname", "info_users", ["nickname"], unique=False
    )
    op.alter_column(
        "info_users", "role_id", existing_type=sa.INTEGER(), nullable=True
    )
