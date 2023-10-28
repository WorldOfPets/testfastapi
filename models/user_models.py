from datetime import datetime
from sqlalchemy import Boolean, Table, Column, Integer, String, TIMESTAMP, ForeignKey
from .metadata import metadata
from .role_models import role, RoleRead
from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from pydantic.version import VERSION as PYDANTIC_VERSION

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

user = Table(
    "user",
    metadata, 
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("hashed_password",String(length=1024), nullable=False),
    Column("is_active",Boolean, default=True, nullable=False),
    Column("is_superuser",Boolean, default=False, nullable=False),
    Column("is_verified",Boolean, default=False, nullable=False),
)

class UserReadBaseModel(BaseModel):
    id: int
    email: EmailStr
    role_id: int
    is_active: bool
    is_superuser: bool
    is_verified: bool

class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    if PYDANTIC_V2:  # pragma: no cover
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:  # pragma: no cover
        class Config:
            orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    role_id: int = Field(default=2)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False



class UserUpdate(schemas.BaseUserUpdate):
    username: str
    email: EmailStr
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
