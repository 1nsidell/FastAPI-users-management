"""'initial'

Revision ID: 8ff1195069f1
Revises:
Create Date: 2025-03-07 20:53:32.279860

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "8ff1195069f1"
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
        sa.Column("role_id", sa.Integer(), nullable=False),
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
            ondelete="SET DEFAULT",
        ),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_info_users")),
    )
    op.create_index(
        op.f("ix_info_users_nickname"), "info_users", ["nickname"], unique=True
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_info_users_nickname"), table_name="info_users")
    op.drop_table("info_users")
    op.drop_table("roles")
