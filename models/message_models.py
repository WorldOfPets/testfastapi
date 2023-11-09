from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from models import Base


class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    message = Column(String)

class MessagesModel(BaseModel):
    id: int
    message: str

    class Config:
        orm_mode = True