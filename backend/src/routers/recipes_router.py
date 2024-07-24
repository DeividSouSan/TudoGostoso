from fastapi import APIRouter, Depends

from ..utils.deps import get_authorization_token
from ..dtos.recipes import Recipe

recipes = APIRouter(prefix="/recipes", tags=["recipes"])

@recipes.get("")
async def get_all(token: dict[str, str] = Depends(get_authorization_token)):
    if token['role'] != 'user':
        return {"message": "You are not authorized to access this resource."}
    
    return {"message": "Here are all the recipes"}
