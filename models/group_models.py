from datetime import datetime
from sqlalchemy import JSON, Boolean, MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, ConfigDict
from models import Base
from typing import  Optional
from uuid import uuid1
from .user_models import User, UserRead
from pydantic.version import VERSION as PYDANTIC_VERSION

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

# role = Table(
#     "role",
#     metadata, 
#     Column("id", Integer, primary_key=True, autoincrement=True),
#     Column("name", String, nullable=False),
#     Column("permissions", String)
# )
class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))
    users=relationship("User", back_populates="groups")

class GroupRead(BaseModel):
    name: str
    user_id: int
    users: Optional[UserRead]

    if PYDANTIC_V2:  # pragma: no cover
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:  # pragma: no cover
        class Config:
            orm_mode = True
    
class GroupCreate(BaseModel):
    id: int = Field(default_factory=lambda: uuid1().time_low)
    name: str
    user_id: int
