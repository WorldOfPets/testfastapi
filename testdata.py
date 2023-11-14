from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from models import Book, Author
from auth.database import engine
import random

import httpx
# Insert data
from sqlalchemy.orm import Session
engine = create_engine("sqlite+pysqlite:///auth/db.sqlite3", future=True, echo=True,
                       connect_args={"check_same_thread": False})
with Session(bind=engine) as session:
    book1 = Book(title="Dead People Who'd Be Influencers Today")
    book2 = Book(title="How To Make Friends In Your 30s")
    
    author1 = Author(name="Blu Renolds")
    author2 = Author(name="Chip Egan")
    author3 = Author(name="Alyssa Wyatt")
    
    book1.authors = [author1, author2]
    book2.authors = [author1, author3]
    
    session.add_all([book1, book2, author1, author2, author3])
    session.commit()


faker = Faker("ru_RU")
address = "http://127.0.0.1:8000"



class CreateTestData:
    def create_role(self):
        callback_url = address + "/roles/"
        try:
            roles = [
                {"id":1, "name":"admin", "permissions":"all"},
                {"id":2, "name":"user", "permissions":"read/write"},
                {"id":3, "name":"unreg", "permissions":"none"}
            ]
            for item in roles:
                result = httpx.post(callback_url, json=item)
            print(result)
        except Exception as ex:
            print(f"Not error: {ex}")

    def create_user(self, user_count: int = 3):
        callback_url = address + "/auth/auth/register"
        try:
            result = httpx.post(callback_url, json={
                "email": "admin@admin.ru",
                "password": "admin",
                "is_active": True,
                "is_superuser": True,
                "is_verified": True,
                "username": "admin",
                "role_id": 1
                })
            for _ in range(user_count):
                result = httpx.post(callback_url, json={
                "email": faker.email(),
                "password": "string",
                "is_active": True,
                "is_superuser": False,
                "is_verified": False,
                "username": faker.name(),
                "role_id": 2
                })
            print(result)
        except Exception as ex:
            print(f"Not error: {ex}")

    def create_task(self, task_count: int = 5, user_in_sys_count: int = 3):
        callback_url = address + "/tasks/"
        try:
            for _ in range(task_count):
                result = httpx.post(callback_url, json={
                    "name": faker.name(),
                    "description": faker.text(),
                    "createdAt": str(faker.date_time()),
                    "author": faker.random.randint(1, user_in_sys_count),
                    "executor": faker.random.randint(1, user_in_sys_count),
                    "deadline": str(datetime.now() + timedelta(days=7)),
                    "difficulty_level": random.uniform(0.0, 10.0),
                    "is_completed": False
                })
            print(result)
        except Exception as ex:
            print(f"Not error: {ex}")

try:
    testdata = CreateTestData()
    # testdata.create_role()
    # testdata.create_user()
    # testdata.create_task()
except Exception as ex:
    print(ex)

# #create 3 role
# create_role()
# #create 3 user
# create_user()
# #create 5 task
# create_task()