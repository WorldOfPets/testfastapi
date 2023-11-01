from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from auth import get_async_session
from models import Task, TaskRead, TaskCreate, TaskUpdate
from typing import List

task_router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@task_router.get("/", response_model=List[TaskRead])
async def get_all_roles(operation_type: str = "", session: AsyncSession = Depends(get_async_session)): 
    query = select(Task)
    result = await session.execute(query)
    return result.all()
    
@task_router.post("/")
async def add_role(new_task:TaskCreate, session: AsyncSession = Depends(get_async_session)):
    query = insert(Task).values(**dict(new_task))
    await session.execute(query)
    await session.commit()
    return {"status":"created"}

@task_router.patch("/{task_id}")
async def update_role(task_id:int, task_update: TaskUpdate, session: AsyncSession = Depends(get_async_session)):
    query = update(Task).where(Task.id == task_id).values(
        name=task_update.name, 
        description=task_update.description,
        executor=task_update.executor, 
        deadline=task_update.deadline, 
        difficulty_level=task_update.difficulty_level, 
        is_completed=task_update.is_completed
        )
    result = await session.execute(query)
    await session.commit()
    return result.last_updated_params()

@task_router.delete("/{task_id}")
async def delete_role(task_id:int, session: AsyncSession = Depends(get_async_session)):
    query = delete(Task).where(Task.id == task_id)
    await session.execute(query)
    await session.commit()
    return {"status":"deleted"}