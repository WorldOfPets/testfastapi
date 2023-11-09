from fastapi import FastAPI, Depends, Request
from auth import get_async_session, engine, User, async_session_maker
from models import Task
from exec import CustomExec
from fastapi.responses import RedirectResponse
from routers import auth_router, utils_router, role_router, task_router, page_router, message_router
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
from fastapi.staticfiles import StaticFiles
passwordHelper = PasswordHelper()
import secrets

#system auth user
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        
        async with async_session_maker() as session:
            session:AsyncSession = session
            query = select(User.hashed_password).where(User.username == username)
            result = await session.execute(query)
        #result = session.execute(query)
        user = result.first()
        if user is not None:
            res = passwordHelper.verify_and_update(password, user[0])
            if res[0]:
                request.session.update({"token":str(secrets.token_urlsafe(16))})
                return True
            else:
                return False
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
#create application 
app = FastAPI(
    title="Trading App",
    version="0.1.1"
)
#set application settings (secret key, auth system)
auth_back = AdminAuth(secret_key="SECRET")
admin  = Admin(app, engine, authentication_backend=auth_back)

#model for admin panel
class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    category = "accounts"
    column_list = [User.id, User.email]
#model for admin panel
class TaskAdmin(ModelView, model=Task):
    column_list = [Task.id, Task.name]
#add table view for admin panel
admin.add_view(TaskAdmin)
admin.add_view(UserAdmin)

#redirect from main to docs
@app.get("/")
#@cache(expire=60)
async def redirect_to_docs(session: AsyncSession = Depends(get_async_session)):
    return RedirectResponse("/docs")

#error handler
CustomExec(app)

#add router in app
app.include_router(role_router)
app.include_router(auth_router)
app.include_router(utils_router)
app.include_router(task_router)
app.include_router(page_router)
app.include_router(message_router)
#add path for static
app.mount("/images", StaticFiles(directory="images"), name="images")

origins = [
    "http://127.0.0.1:5500",
]
#add middleware (defender)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

# @app.on_event("startup")
# async def startup():
#     #NEED REDIS
#     #redis = aioredis.from_url("redis://localhost")
#     #FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#     pass