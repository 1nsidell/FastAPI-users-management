"""init

Revision ID: 9f1e4e457446
Revises:
Create Date: 2025-03-14 17:24:46.678455

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "9f1e4e457446"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "info_users",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("nickname", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("avatar", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_info_users")),
    )
    op.create_index(
        op.f("ix_info_users_nickname"), "info_users", ["nickname"], unique=True
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_info_users_nickname"), table_name="info_users")
    op.drop_table("info_users")
