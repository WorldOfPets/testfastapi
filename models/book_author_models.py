"""
FastAPI app called 'Bookipedia' that serves information about books and their authors. A simple example of a
"many-to-many" relationship *without* extra data.
"""

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from models import Base
from pydantic import BaseModel, ConfigDict
from pydantic.version import VERSION as PYDANTIC_VERSION

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")



# Declare Classes / Tables
book_authors = Table('book_authors', Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('author_id', ForeignKey('authors.id'), primary_key=True)
)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    authors = relationship("Author", secondary="book_authors", back_populates='books')

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    books = relationship("Book", secondary="book_authors", back_populates='authors')

class AuthorBase(BaseModel):
    id: int
    name: str

    if PYDANTIC_V2:  # pragma: no cover
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:  # pragma: no cover
        class Config:
            orm_mode = True
    

class BookBase(BaseModel):
    id: int
    title: str

    if PYDANTIC_V2:  # pragma: no cover
        model_config = ConfigDict(from_attributes=True)  # type: ignore
    else:  # pragma: no cover
        class Config:
            orm_mode = True
    

class BookSchema(BookBase):
    authors: list[AuthorBase]

class AuthorSchema(AuthorBase):
    books: list[BookBase]