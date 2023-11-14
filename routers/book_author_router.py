from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from auth import get_async_session
from models import Group, GroupCreate, GroupRead
from typing import List
from models import  BookSchema, AuthorSchema, Book, Author, BookBase, AuthorBase

book_author_router = APIRouter(
    prefix="/ba",
    tags=["Books Authors"]
)



@book_author_router.get("/books/{id}", response_model=BookSchema)
async def get_book(id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Book).options(selectinload(Book.authors)).where(Book.id == id)
    result = await session.execute(query)
    # db_book = session.query(Book).options(joinedload(Book.authors)).\
    #     where(Book.id == id).one()
    return result.scalar()


@book_author_router.get("/books", response_model=List[BookSchema])
async def get_books(session: AsyncSession = Depends(get_async_session)):
    query = select(Book).options(selectinload(Book.authors))
    result = await session.execute(query)
    return result.scalars()
    # db_books = session.query(Book).options(joinedload(Book.authors)).all()
    # return db_books


@book_author_router.get("/authors/{id}", response_model=AuthorSchema)
async def get_author(id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Author).options(selectinload(Author.books)).where(Author.id == id)
    result = await session.execute(query)
    return result.scalar()
    # db_author = session.query(Author).options(joinedload(Author.books)).where(Author.id == id).one()
    # return db_author


@book_author_router.get("/authors", response_model=List[AuthorSchema])
async def get_authors(session: AsyncSession = Depends(get_async_session)):
    query = select(Author).options(selectinload(Author.books))
    result = await session.execute(query)
    return result.scalars()
    # db_authors = session.query(Author).options(joinedload(Author.books)).all()
    # return db_authors