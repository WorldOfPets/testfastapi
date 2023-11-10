from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from auth import User, get_user_manager, auth_backend
from models import UserRead, UserCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth import get_async_session

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["Auth"],
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
