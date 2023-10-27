from typing import List
from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from schemas import Trade, User
from testdata import *
from exec import CustomExec
from auth.auth import auth_backend
from routers.role_router import role_router

app = FastAPI(
    title="Trading App",
    version="0.1.1"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

CustomExec(app)

app.include_router(role_router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

current_user = fastapi_users.current_user()

@app.get("/test-auth")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/test")
def unprotected_route():
    return f"Hello, anonym"