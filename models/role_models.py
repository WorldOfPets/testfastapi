from datetime import datetime
from sqlalchemy import JSON, Boolean, MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey
from pydantic import BaseModel
from .metadata import metadata


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

class RoleUpdate(BaseModel):
    name: str
    permissions: str
