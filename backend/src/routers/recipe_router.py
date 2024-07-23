from fastapi import APIRouter, Depends

from ..utils.deps import get_authorization_token
from ..dtos.recipes import Recipe

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("")
async def get_all(token: str = Depends(get_authorization_token)):
    return token
