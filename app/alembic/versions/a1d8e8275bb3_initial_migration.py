"""Initial migration

Revision ID: a1d8e8275bb3
Revises: 
Create Date: 2025-04-08 08:29:22.961461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1d8e8275bb3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tables',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('seats', sa.Integer(), nullable=False),
    sa.Column('location', sa.Enum('MAIN_HALL', 'TERRACE', 'GARDEN', 'PRIVATE_ROOM', 'BAR_AREA', name='tablelocation'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_tables_id'), 'tables', ['id'], unique=False)
    op.create_table('reservations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_name', sa.String(), nullable=False),
    sa.Column('table_id', sa.Integer(), nullable=False),
    sa.Column('reservation_time', sa.DateTime(), nullable=False),
    sa.Column('duration_minutes', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['table_id'], ['tables.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reservations_id'), 'reservations', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reservations_id'), table_name='reservations')
    op.drop_table('reservations')
    op.drop_index(op.f('ix_tables_id'), table_name='tables')
    op.drop_table('tables')
    # ### end Alembic commands ###
