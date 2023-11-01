from fastapi import FastAPI, Depends, Request
from auth import get_async_session, engine, User, async_session_maker
from models import Task
from exec import CustomExec
from fastapi.responses import RedirectResponse
from routers import auth_router, utils_router, role_router, task_router
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi_users.password import PasswordHelper
passwordHelper = PasswordHelper()
import secrets


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        print(passwordHelper.hash(password))
        async with async_session_maker() as session:
            session:AsyncSession = session
            query = select(User).where(User.username == username)
            result = await session.execute(query)
        #result = session.execute(query)
        user = result.first()
        if user is not None:
            print(user.hashed_password)
            request.session.update({"token":str(secrets.token_urlsafe(16))})
            return True
        else:
            return False
    
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        print(token)
        if not token:
            return False
        return True

app = FastAPI(
    title="Trading App",
    version="0.1.1"
)
auth_back = AdminAuth(secret_key="SECRET")
admin  = Admin(app, engine, authentication_backend=auth_back)


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    category = "accounts"
    column_list = [User.id, User.email]

class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.name]

admin.add_view(TaskAdmin)
admin.add_view(UserAdmin)


@app.get("/")
#@cache(expire=60)
async def redirect_to_docs(session: AsyncSession = Depends(get_async_session)):
    return RedirectResponse("/docs")

CustomExec(app)

app.include_router(role_router)
app.include_router(auth_router)
app.include_router(utils_router)
app.include_router(task_router)

origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.on_event("startup")
async def startup():
    #NEED REDIS
    #redis = aioredis.from_url("redis://localhost")
    #FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    pass