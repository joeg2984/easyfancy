"""Make ingredients optional

Revision ID: 2e53164e9b70
Revises: 89440140396e
Create Date: 2024-10-12 19:38:42.680695

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e53164e9b70'
down_revision: Union[str, None] = '89440140396e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_houses_id', table_name='houses')
    op.drop_table('houses')
    op.drop_index('ix_wolves_id', table_name='wolves')
    op.drop_table('wolves')
    op.drop_index('ix_pigs_id', table_name='pigs')
    op.drop_table('pigs')
    op.drop_index('ix_chefs_chef_id', table_name='chefs')
    op.drop_table('chefs')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chefs',
    sa.Column('chef_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('chef_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('chef_specialty', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('chef_experience', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('chef_michelin_stars', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('chef_restaurant', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('chef_rating', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('chef_id', name='chefs_pkey')
    )
    op.create_index('ix_chefs_chef_id', 'chefs', ['chef_id'], unique=False)
    op.create_table('pigs',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('pigs_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('pig_house', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('pig_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('pig_color', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('pig_hoof_count', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='pigs_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_pigs_id', 'pigs', ['id'], unique=False)
    op.create_table('wolves',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('wolf_power', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('wolf_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='wolves_pkey')
    )
    op.create_index('ix_wolves_id', 'wolves', ['id'], unique=False)
    op.create_table('houses',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('sturdiness', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('pig_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('address', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['pig_id'], ['pigs.id'], name='houses_pig_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='houses_pkey')
    )
    op.create_index('ix_houses_id', 'houses', ['id'], unique=False)
    # ### end Alembic commands ###
