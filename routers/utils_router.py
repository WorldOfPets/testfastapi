from fastapi import APIRouter, Depends
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

@utils_router.get("/create-test-data")
async def create_test_data(task_count: int = 20, user_count: int = 2, role_count: int = 3, session: AsyncSession = Depends(get_async_session)):
    for _ in range(task_count):
        new_task = TaskCreate(name=faker.name(), description=faker.text(), author=faker.random.randint(1, 2), executor=faker.random.randint(1, 2))
        query_task = insert(task).values(dict(new_task))
        await session.execute(query_task)
        await session.commit()
    return f"f"

@utils_router.get("/test-auth")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@utils_router.get("/test")
def unprotected_route():
    return f"Hello, anonym"