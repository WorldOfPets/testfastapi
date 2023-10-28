from fastapi import APIRouter, Depends
from auth import User
from .auth_router import current_user

utils_router = APIRouter(
    prefix="/utils",
    tags=["Utils"]
)

@utils_router.get("/test-auth")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@utils_router.get("/test")
def unprotected_route():
    return f"Hello, anonym"