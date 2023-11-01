from fastapi import APIRouter, Depends, HTTPException
import httpx
from auth import User
from .auth_router import current_user
from faker import Faker

faker = Faker("ru_RU")

utils_router = APIRouter(
    prefix="/utils",
    tags=["Utils"]
)


    

@utils_router.get("/test-auth")
def protected_route(user: User = Depends(current_user)):
    try:    
        return f"Hello, {user.username}"
    except Exception as ex:
            raise HTTPException(status_code=555, detail=ex)


@utils_router.get("/test")
def unprotected_route():
    try:    
        x = 10 / 0
        return f"Hello, {x}"
    except Exception as ex:
        raise HTTPException(status_code=555, detail=str(ex))