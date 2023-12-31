from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from auth import get_async_session
from models import Role, RoleCreate, RoleRead, RoleUpdate
from typing import List

role_router = APIRouter(
    prefix="/roles",
    tags=["Role"]
)

@role_router.get("/", response_model=list[RoleRead])
async def get_all_roles(operation_type: str = "", session: AsyncSession = Depends(get_async_session)): 
    query = select(Role)
    result = await session.execute(query)
    return result.scalars()
    
@role_router.post("/")
async def add_role(new_role:RoleCreate, session: AsyncSession = Depends(get_async_session)):
    query = insert(Role).values(**dict(new_role))
    print(query)
    await session.execute(query)
    await session.commit()
    return {"status":"created"}

@role_router.patch("/{role_id}")
async def update_role(role_id:int, update_role: RoleUpdate, session: AsyncSession = Depends(get_async_session)):
    query = update(Role).where(Role.id == role_id).values(name=update_role.name, permissions=update_role.permissions)
    result = await session.execute(query)
    await session.commit()
    return result.last_updated_params()

@role_router.delete("/{role_id}")
async def delete_role(role_id:int, session: AsyncSession = Depends(get_async_session)):
    query = delete(Role).where(Role.id == role_id)
    await session.execute(query)
    await session.commit()
    return {"status":"deleted"}