from fastapi import FastAPI, Depends
from auth import get_async_session
from exec import CustomExec
from fastapi.responses import RedirectResponse
from routers import auth_router, utils_router, role_router, task_router
from sqlalchemy.ext.asyncio import AsyncSession
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Trading App",
    version="0.1.1"
)



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