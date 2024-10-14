import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from db import engine, get_session
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.recipe_ingredient_link import RecipeIngredientLink
from sqlalchemy import func, distinct
from fastapi.encoders import jsonable_encoder
import inflect
from rapidfuzz import process, fuzz

app = FastAPI(debug=True)
p = inflect.engine()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/recipes/suggest", response_model=List[Recipe])
def suggest_recipes(user_input: str, session: Session = Depends(get_session)):
    user_ingredients = [ing.strip().lower() for ing in user_input.split(',') if ing.strip()]
    if not user_ingredients:
        raise HTTPException(status_code=400, detail="No ingredients found in the input.")
    print(f"User-provided ingredients: {user_ingredients}")
    db_ingredients = session.exec(select(Ingredient.ingredient_name)).all()
    db_ingredients = [ing.lower() for ing in db_ingredients]
    mapped_ingredients = []
    for user_ing in user_ingredients:
        match, score, _ = process.extractOne(user_ing, db_ingredients, scorer=fuzz.WRatio)
        if score >= 80:
            mapped_ingredients.append(match)
            print(f"Matched '{user_ing}' to '{match}' with score {score}")
        else:
            print(f"No close match found for ingredient: '{user_ing}' (Score: {score})")
    mapped_ingredients = list(set(mapped_ingredients))
    if not mapped_ingredients:
        raise HTTPException(status_code=404, detail="No matching ingredients found in the database.")
    print(f"Mapped ingredients: {mapped_ingredients}")
    statement = (
        select(Recipe)
        .join(RecipeIngredientLink)
        .join(Ingredient)
        .where(func.lower(Ingredient.ingredient_name).in_(mapped_ingredients))
        .group_by(Recipe.id)
        .having(func.count(distinct(Ingredient.id)) == len(mapped_ingredients))
    )
    recipes = session.exec(statement).all()
    print(f"Number of recipes found: {len(recipes)}")
    for recipe in recipes:
        print(f"Recipe found: {recipe.name}")
    for recipe in recipes:
        session.refresh(recipe)
    return jsonable_encoder(recipes)

@app.post("/recipe/add", response_model=Recipe)
def add_recipe(recipe: Recipe, session: Session = Depends(get_session)):
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    return recipe

def get_recipe(recipe_id: int, session: Session = Depends(get_session)):
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.put("/recipe/update/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, recipe: Recipe, session: Session = Depends(get_session)):
    db_recipe = session.get(Recipe, recipe_id)
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    update_data = recipe.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_recipe, key, value)
    session.add(db_recipe)
    session.commit()
    session.refresh(db_recipe)
    return db_recipe

@app.post("/ingredient/add", response_model=Ingredient)
def add_ingredient(ingredient: Ingredient, session: Session = Depends(get_session)):
    session.add(ingredient)
    session.commit()
    session.refresh(ingredient)
    return ingredient

@app.put("/ingredient/update/{ingredient_id}", response_model=Ingredient)
def update_ingredient(ingredient_id: int, ingredient: Ingredient, session: Session = Depends(get_session)):
    db_ingredient = session.get(Ingredient, ingredient_id)
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    update_data = ingredient.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ingredient, key, value)
    session.add(db_ingredient)
    session.commit()
    session.refresh(db_ingredient)
    return db_ingredient

@app.delete("/recipe/{recipe_id}/delete", response_model=Recipe)
def delete_recipe(recipe_id: int, session: Session = Depends(get_session)):
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    session.delete(recipe)
    session.commit()
    return recipe

@app.post("/recipe/{recipe_id}/add_ingredient", response_model=RecipeIngredientLink)
def add_ingredient_to_recipe(recipe_id: int, ingredient_id: int, session: Session = Depends(get_session)):
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    ingredient = session.get(Ingredient, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    ingredient_link = RecipeIngredientLink(
        recipe_id=recipe_id,
        ingredient_id=ingredient_id
    )
    session.add(ingredient_link)
    session.commit()
    session.refresh(ingredient_link)
    return ingredient_link

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
