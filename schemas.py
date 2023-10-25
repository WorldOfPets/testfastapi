from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str
    side: str
    price: float = Field(ge=0, default=100.2)
    amount: float

class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"

class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType

class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] 


