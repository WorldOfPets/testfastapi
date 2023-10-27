from typing import List
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from schemas import Trade, User
from testdata import *
from exec import CustomExec
from auth.auth import auth_backend
from routers.role_router import role_router

app = FastAPI(
    title="Trading App",
    version="0.1.1"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

CustomExec(app)

app.include_router(role_router)

# @app.get("/users/{user_id}", response_model=List[User])
# def hello(user_id: int):
#     # u_array = []
#     # for user in fake_users:
#     #     if user_id == user.get("role"):
#     #         u_array.append(user)
#     # return u_array
#     return [user for user in fake_users if user_id == user.get("id")]

# @app.get("/trades", response_model=Trade)
# def get_trades(limit: int = 1, offset: int = 0):
#     return fake_trades[offset:][:limit]

# @app.post("/users/{user_id}")
# def change_user_name(user_id: int, new_name: str):
#     current_user = list(filter(lambda user: user.get("id") == user_id, fake_users))[0]
#     current_user["name"] = new_name
#     return {"status": 200, "data":current_user}

# @app.post("/trades")
# def add_trades(trades: Trade):
#     fake_trades.append(trades)
#     return {"status":200, "data":fake_trades}

# @app.post("/role")
# async def add_role(new_operation: RoleCreate, session: AsyncSession = Depends(get_async_session)):
#     stmt = insert(operation).values(**new_operation.dict())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": "success"}

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)