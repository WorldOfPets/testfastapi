from fastapi import APIRouter, Depends, HTTPException
import httpx
from auth import User
from .auth_router import current_user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, update
from auth import get_async_session, get_user_manager
from models import role, task, user, RoleCreate, TaskCreate
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
            raise HTTPException(status_code=666, detail=ex)


@utils_router.get("/test")
def unprotected_route():
    try:    
        x = 10 / 0
        return f"Hello, {x}"
    except Exception as ex:
        raise HTTPException(status_code=555, detail=str(ex))