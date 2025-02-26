"""init

Revision ID: 38d83670f4ba
Revises:
Create Date: 2025-02-26 19:40:46.963942

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "38d83670f4ba"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("role_id", name=op.f("pk_roles")),
        sa.UniqueConstraint("role", name=op.f("uq_roles_role")),
    )
    op.create_table(
        "info_users",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.Column("nickname", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("avatar", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.role_id"],
            name=op.f("fk_info_users_role_id_roles"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_info_users")),
    )
    op.create_index(
        op.f("ix_info_users_nickname"),
        "info_users",
        ["nickname"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_info_users_nickname"), table_name="info_users")
    op.drop_table("info_users")
    op.drop_table("roles")
