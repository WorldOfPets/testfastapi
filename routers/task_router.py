from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from auth import get_async_session
from models import task, TaskRead, TaskCreate
from typing import List

task_router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@task_router.get("/", response_model=List[TaskRead])
async def get_all_roles(operation_type: str = "", session: AsyncSession = Depends(get_async_session)): 
    query = select(task)
    result = await session.execute(query)
    return result.all()
    
@task_router.post("/")
async def add_role(new_task:TaskCreate, session: AsyncSession = Depends(get_async_session)):
    query = insert(task).values(**dict(new_task))
    await session.execute(query)
    await session.commit()
    return {"status":"created"}

# @task_router.patch("/{role_id}")
# async def update_role(role_id:int, update_role: RoleUpdate, session: AsyncSession = Depends(get_async_session)):
#     query = update(role).where(role.c.id == role_id).values(name=update_role.name, permissions=update_role.permissions)
#     result = await session.execute(query)
#     await session.commit()
#     return result.last_updated_params()

# @task_router.delete("/{role_id}")
# async def delete_role(role_id:int, session: AsyncSession = Depends(get_async_session)):
#     query = delete(role).where(role.c.id == role_id)
#     await session.execute(query)
#     await session.commit()
#     return {"status":"deleted"}