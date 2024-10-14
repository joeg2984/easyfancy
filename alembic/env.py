from logging.config import fileConfig

from sqlalchemy import pool
from alembic import context
from sqlmodel import SQLModel  # Import SQLModel

# Import your models so Alembic can see them and autogenerate migrations
from db import engine  # Import the engine from your db module
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.recipe_ingredient_link import RecipeIngredientLink

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = SQLModel.metadata  # Set to SQLModel metadata

# other values from the config, defined by the needs of env.py, can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Use the engine from your db module
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,  # Ensure Alembic considers changes to column types
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
