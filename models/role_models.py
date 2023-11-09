from datetime import datetime
from sqlalchemy import JSON, Boolean, MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey
from pydantic import BaseModel, Field
from .metadata import Base
from typing import  Optional
from uuid import uuid1

# role = Table(
#     "role",
#     metadata, 
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("name", String, nullable=False),
#     Column("permissions", String)
# )
class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    permissions = Column(String)

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
