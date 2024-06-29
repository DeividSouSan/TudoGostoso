from fastapi import APIRouter
from schemas.users import User

user_router = APIRouter(prefix="/recipes", tags=["user"])


@user_router.get("/get-users")
async def get_recipes():
    return {"response": "all recipes"}


@user_router.post("/add-user")
async def add_recipe(user: User):
    return User


@user_router.put("/update-user/{user_id}")
async def update_recipe(user_id: int):
    return {"response": f"updated recipe {user_id}"}


@user_router.delete("/delete-user/{user_id}")
async def delete_recipe(user_id: int):
    return {"response": f"deleted recipe {user_id}"}
