
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional, TYPE_CHECKING
from models.recipe_ingredient_link import RecipeIngredientLink

if TYPE_CHECKING:
    from models.ingredient import Ingredient

class Recipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    time_estimate: int  # In minutes
    instructions: str
    history: str
    cuisine: str

    ingredients: List["Ingredient"] = Relationship(
        back_populates="recipes",
        link_model=RecipeIngredientLink,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class RecipeRead(SQLModel):
    id: int
    name: str
    time_estimate: int
    instructions: str
    history: str
    cuisine: str
    ingredients: List["IngredientRead"]

class IngredientRead(SQLModel):
    id: int
    ingredient_name: str
    quantity: Optional[str] = None
