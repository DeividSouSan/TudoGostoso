from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from .src.routers.auth_router import auth_router
from .src.routers.recipes_router import recipes_router
from .src.routers.users_router import users_router

app = FastAPI(
    title="TudoGostoso",
    description="An API made for users share recipes with each other.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Users", "description": "Routes related to user entity manipulation."},
        {
            "name": "Recipes",
            "description": "Routes related to recipe entity manipulation.",
        },
        {
            "name": "Auth",
            "description": "Routes related to user authentication.",
        },
    ],
    openapi_components={
        "securitySchemes": {
            "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        }
    },
    openapi_security=[{"BearerAuth": []}],
)


app.include_router(users_router)
app.include_router(recipes_router)
app.include_router(auth_router)


def create_tables():
    from .src.db.base import Base
    from .src.db.connection import engine

    Base.metadata.create_all(bind=engine)


create_tables()
