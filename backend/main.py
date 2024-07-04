from fastapi import FastAPI, Request
from routers.recipe_router import recipe_router
from routers.user_router import user_router


app = FastAPI()


def create_tables():
    from models.recipe import Recipe
    from models.user import User

    import database
    database.Base.metadata.create_all(bind=database.engine)
    
create_tables()


app.include_router(recipe_router)
app.include_router(user_router)
