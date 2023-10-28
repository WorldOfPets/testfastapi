from datetime import datetime
from sqlalchemy import JSON, Boolean, MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey
from pydantic import BaseModel, Field
from .metadata import metadata
from typing import  Optional
from uuid import uuid1

role = Table(
    "role",
    metadata, 
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("permissions", String)
)

class RoleRead(BaseModel):
    name: str
    permissions: str
    
class RoleCreate(BaseModel):
    id: int = Field(default_factory=lambda: uuid1().time_low)
    name: str
    permissions: str

class RoleUpdate(BaseModel):
    name: str
    permissions: str
