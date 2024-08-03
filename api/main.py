from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from .src.routers.auth_router import auth_router
from .src.routers.recipes_router import recipes_router
from .src.routers.users_router import users_router

app = FastAPI()

app.include_router(users_router)
app.include_router(recipes_router)
app.include_router(auth_router)


def create_tables():
    from .src.db.base import Base
    from .src.db.connection import engine

    Base.metadata.create_all(bind=engine)


create_tables()
