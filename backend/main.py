from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from .src.routers.recipes_router import recipes
from .src.routers.users_router import users
from fastapi.encoders import jsonable_encoder

app = FastAPI()

app.include_router(users)
app.include_router(recipes)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors()})
    )

@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors()})
    )


def create_tables():
    import backend.src.db.base as base
    from backend.src.db.connection import engine
    from backend.src.models.recipe import Recipe
    from backend.src.models.user import User

    base.Base.metadata.create_all(bind=engine)


create_tables()



