from datetime import datetime
from sqlalchemy import JSON, Boolean, MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey
from pydantic import BaseModel

metadata = MetaData()

role = Table(
    "role",
    metadata, 
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("permissions", String)
)
class RoleRead(BaseModel):
    id: int
    name: str
    permissions: str
    
class RoleCreate(BaseModel):
    id: int
    name: str
    permissions: str

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
