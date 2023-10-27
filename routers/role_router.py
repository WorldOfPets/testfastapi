from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from auth.database import get_async_session
from models.models import role, RoleCreate, RoleRead
from typing import List

role_router = APIRouter(
    prefix="/roles",
    tags=["Role"]
)

@role_router.get("/", response_model=List[RoleRead])
async def get_all_roles(operation_type: str = "", session: AsyncSession = Depends(get_async_session)): 
    query = select(role)
    result = await session.execute(query)
    return result.all()
    
@role_router.post("/")
async def add_role(new_role:RoleCreate, session: AsyncSession = Depends(get_async_session)):
    query = insert(role).values(**dict(new_role))
    print(query)
    await session.execute(query)
    await session.commit()
    return {"status":"ok"}