"""Add ingredients relationship

Revision ID: 89440140396e
Revises: 4000a8447faa
Create Date: 2024-10-12 19:28:31.765946

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89440140396e'
down_revision: Union[str, None] = '4000a8447faa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_dishes_dish_id', table_name='dishes')
    op.drop_table('dishes')
    op.drop_index('ix_restaurant_restaurant_id', table_name='restaurant')
    op.drop_table('restaurant')
    op.drop_constraint('ingredient_recipe_id_fkey', 'ingredient', type_='foreignkey')
    op.drop_column('ingredient', 'recipe_id')
    op.drop_column('recipe', 'ingredients')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('ingredients', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('ingredient', sa.Column('recipe_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('ingredient_recipe_id_fkey', 'ingredient', 'recipe', ['recipe_id'], ['id'])
    op.create_table('restaurant',
    sa.Column('restaurant_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('restaurant_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('restaurant_cuisine', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('restaurant_rating', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('restaurant_chef', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('restaurant_dishes', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('restaurant_ingredients', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('restaurant_location', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('restaurant_price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('restaurant_michelin_stars', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('restaurant_id', name='restaurant_pkey')
    )
    op.create_index('ix_restaurant_restaurant_id', 'restaurant', ['restaurant_id'], unique=False)
    op.create_table('dishes',
    sa.Column('dish_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('dish_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('dish_cuisine', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('dish_price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('dish_rating', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('dish_chef', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('dish_restaurant', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('dish_ingredients', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('dish_id', name='dishes_pkey')
    )
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
