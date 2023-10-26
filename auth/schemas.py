from typing import Optional
import uuid

from fastapi_users import schemas
from pydantic import EmailStr, ConfigDict, BaseModel
from pydantic.version import VERSION as PYDANTIC_VERSION
from sqlalchemy import JSON

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

class UserRead(schemas.BaseUser[int]):
    id: int
    email: EmailStr
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
    role_id: int
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

class RoleCreate(BaseModel):
    name: str
    permissions: str