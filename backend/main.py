from fastapi import FastAPI, Request
from src.routers.recipe_router import recipe_router
from src.routers.user_router import user_router

app = FastAPI()


def create_tables():
    import src.db.base as base
    from src.db.connection import engine
    from src.models.recipe import Recipe
    from src.models.user import User

    base.Base.metadata.create_all(bind=engine)


create_tables()


app.include_router(recipe_router)
app.include_router(user_router)
