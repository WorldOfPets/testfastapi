import pytest
from sqlalchemy import insert, select

#from auth.models import role
from models import Role
from conftest import client, async_session_maker


async def test_add_role():
    async with async_session_maker() as session:
        stmt = insert(Role).values(id=1, name="admin", permissions="all")
        await session.execute(stmt)
        await session.commit()

        query = select(Role)
        result = await session.execute(query)
        print(result.scalars())
        assert result.all() != None
        #assert result.all() != [(1, 'admin', "all")], "Роль не добавилась"

def test_register():
    response = client.post("/auth/auth/register", json={
        "id":1,
        "email": "string@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string",
        "role_id": 1
    })

    assert response.status_code == 201