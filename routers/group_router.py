from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from auth import get_async_session
from models import Group, GroupCreate, GroupRead
from typing import List
from models import User

group_router = APIRouter(
    prefix="/groups",
    tags=["group"]
)

@group_router.get("/", response_model=list[GroupRead])
async def get_all_groups(operation_type: str = "", session: AsyncSession = Depends(get_async_session)): 
    query = select(Group).options(selectinload(Group.users))
    result = await session.execute(query)
    return result.scalars()

@group_router.get("/{group_id}", response_model=GroupRead)
async def get_group(group_id: int, session: AsyncSession = Depends(get_async_session)): 
    query = select(Group).where(Group.id == group_id)
    result = await session.execute(query)
    return result.scalar()
    
@group_router.post("/")
async def add_group(new_group:GroupCreate, session: AsyncSession = Depends(get_async_session)):
    query = insert(Group).values(**dict(new_group))
    print(query)
    await session.execute(query)
    await session.commit()
    return {"status":"created"}

# @group_router.patch("/{group_id}")
# async def update_group(group_id:int, update_group: groupUpdate, session: AsyncSession = Depends(get_async_session)):
#     query = update(group).where(group.id == group_id).values(name=update_group.name, permissions=update_group.permissions)
#     result = await session.execute(query)
#     await session.commit()
#     return result.last_updated_params()

@group_router.delete("/{group_id}")
async def delete_group(group_id:int, session: AsyncSession = Depends(get_async_session)):
    query = delete(Group).where(Group.id == group_id)
    await session.execute(query)
    await session.commit()
    return {"status":"deleted"}