from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING
from models.recipe_ingredient_link import RecipeIngredientLink

if TYPE_CHECKING:
    from models.recipe import Recipe
    from models.recipe_ingredient_link import RecipeIngredientLink

class Ingredient(SQLModel, table=True):
    # Define the fields of the Ingredient model. The id field is the primary key. 
    # The recipes field is a list of Recipe objects, which is a many-to-many relationship.
    id: Optional[int] = Field(default=None, primary_key=True)
    

    ingredient_name: str
    quantity: Optional[str] = None

    # Many-to-many relationship with Recipe through RecipeIngredientLink
    recipes: List["Recipe"] = Relationship(back_populates="ingredients", link_model=RecipeIngredientLink)
