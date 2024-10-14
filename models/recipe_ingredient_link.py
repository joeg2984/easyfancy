# many to many relationship between recipes and ingredients

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class RecipeIngredientLink(SQLModel, table=True):
    recipe_id: Optional[int] = Field(default=None, foreign_key="recipe.id", primary_key=True)
    ingredient_id: Optional[int] = Field(default=None, foreign_key="ingredient.id", primary_key=True)
