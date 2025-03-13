"""init

Revision ID: e7642893005b
Revises:
Create Date: 2025-03-10 08:33:27.175257

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e7642893005b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_info_users_nickname"), table_name="info_users")
    op.drop_table("info_users")
    # ### end Alembic commands ###
