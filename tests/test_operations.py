from httpx import AsyncClient
from faker import Faker
faker = Faker("ru_RU")
from datetime import datetime, timedelta
import random

async def test_add_specific_operations(ac: AsyncClient):
    response = await ac.post("/tasks/", json={
                    "name": "task name",
                    "description": "task description",
                    "createdAt": str(datetime.now()),
                    "author": 1,
                    "executor": 1,
                    "deadline": str(datetime.now() + timedelta(days=7)),
                    "difficulty_level": random.uniform(0.0, 10.0),
                    "is_completed": False
                })

    assert response.status_code == 200

async def test_get_specific_operations(ac: AsyncClient):
    response = await ac.get("/tasks/", params={
        "operation_type": "Anything",
    })

    assert response.status_code == 200
    assert response.json()[0]["is_completed"] == False
    #assert len(response.json()[0]["author"]) == 1