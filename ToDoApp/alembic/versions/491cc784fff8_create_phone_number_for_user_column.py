"""create phone-number for user column

Revision ID: 491cc784fff8
Revises: 
Create Date: 2025-07-31 15:56:16.419890

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import exc


# revision identifiers, used by Alembic.
revision: str = '491cc784fff8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    try:
        columns = {col["name"] for col in inspector.get_columns("users")}
        if "phoneNumber" not in columns:
            op.add_column('users', sa.Column('phoneNumber', sa.String(), nullable=True))
    except exc.NoSuchTableError:
        # Fresh DB: create base tables for users/todos
        op.create_table(
            'users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(length=255), nullable=True),
            sa.Column('username', sa.String(length=255), nullable=True),
            sa.Column('firstname', sa.String(length=255), nullable=True),
            sa.Column('lastname', sa.String(length=255), nullable=True),
            sa.Column('hashed_password', sa.String(length=255), nullable=True),
            sa.Column('is_active', sa.Boolean(), nullable=True),
            sa.Column('role', sa.String(length=50), nullable=True),
            sa.Column('phoneNumber', sa.String(length=50), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email'),
            sa.UniqueConstraint('username'),
        )
        op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

        op.create_table(
            'todos',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(), nullable=True),
            sa.Column('description', sa.String(), nullable=True),
            sa.Column('priority', sa.Integer(), nullable=True),
            sa.Column('complete', sa.Boolean(), nullable=True),
            sa.Column('owner_id', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['owner_id'], ['users.id']),
            sa.PrimaryKeyConstraint('id'),
        )
        op.create_index(op.f('ix_todos_id'), 'todos', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    try:
        columns = {col["name"] for col in inspector.get_columns("users")}
        if "phoneNumber" in columns:
            op.drop_column('users', 'phoneNumber')
    except exc.NoSuchTableError:
        # If the table didn't exist, nothing to downgrade
        return
