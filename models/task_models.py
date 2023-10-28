from datetime import datetime
from typing import Optional, Union
from uuid import uuid1
from sqlalchemy import JSON, Boolean, MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Float
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict
from .metadata import metadata
from .user_models import user, UserReadBaseModel, UserRead
from pydantic.version import VERSION as PYDANTIC_VERSION
from sqlalchemy.ext.declarative import declarative_base


PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

task = Table(
    "task",
    metadata, 
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("createdAt", TIMESTAMP, default=datetime.now()),
    Column("author", Integer, ForeignKey(user.c.id)),
    Column("executor", Integer, ForeignKey(user.c.id), nullable=True),
    Column("deadline", TIMESTAMP, nullable=True),
    Column("difficulty_level", Float, default=0.0),
    Column("is_completed", Boolean, default=False)
)

class TaskRead(BaseModel):
    id: int
    name: str
    description: str
    createdAt: datetime
    author: int
    executor: int
    deadline: datetime
    difficulty_level: float
    is_completed: bool

    if PYDANTIC_V2:  # pragma: no cover
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:  # pragma: no cover
        class Config:
            orm_mode = True
    
class TaskCreate(BaseModel):
    id: int = Field(default_factory=lambda: uuid1().time_low)
    name: str
    description: str
    createdAt: Optional[datetime] = datetime.now()
    author: int
    executor: int
    deadline: Optional[datetime] = datetime.now()
    difficulty_level: float = Field(gt=0, lt=10, default=1.0)
    is_completed: Optional[bool] = False


class TaskUpdate(BaseModel):
    name: str
    permissions: str