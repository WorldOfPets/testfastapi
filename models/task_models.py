from datetime import datetime
from typing import Optional, Union
from uuid import uuid1
from sqlalchemy import JSON, Boolean, MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Float
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict
from .metadata import metadata, Base
from .user_models import User, UserReadBaseModel, UserRead
from pydantic.version import VERSION as PYDANTIC_VERSION

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

# task = Table(
#     "task",
#     metadata, 
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("name", String, nullable=False),
#     Column("description", String),
#     Column("createdAt", TIMESTAMP, default=datetime.now()),
#     Column("author", Integer, ForeignKey(user.c.id)),
#     Column("executor", Integer, ForeignKey(user.c.id), nullable=True),
#     Column("deadline", TIMESTAMP, nullable=True),
#     Column("difficulty_level", Float, default=0.0),
#     Column("is_completed", Boolean, default=False)
# )
class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    createdAt = Column(TIMESTAMP, default=datetime.now())
    author = Column(Integer, ForeignKey(User.id))
    executor = Column(Integer, ForeignKey(User.id), nullable=True)
    deadline = Column(TIMESTAMP, nullable=True)
    difficulty_level = Column(Float, default=0.0)
    is_completed = Column(Boolean, default=False)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TaskRead(BaseModel):
    id: int
    name: str
    description: str
    createdAt: datetime
    author: UserRead
    executor: Optional[UserRead]
    deadline: datetime
    difficulty_level: float
    is_completed: bool
    

    

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
    description: str
    executor: int
    deadline: datetime
    difficulty_level: float
    is_completed: bool