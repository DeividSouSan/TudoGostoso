from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from .src.routers.recipes_router import recipes
from .src.routers.users_router import users

app = FastAPI()

app.include_router(users)
app.include_router(recipes)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422, content=jsonable_encoder({"detail": exc.errors()})
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400, content=jsonable_encoder({"detail": exc.errors()})
    )


def create_tables():
    from .src.db.base import Base
    from .src.db.connection import engine
    from .src.models.recipes import Recipe
    from .src.models.users import User

    Base.metadata.create_all(bind=engine)


create_tables()
