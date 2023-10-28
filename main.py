from fastapi import FastAPI, Depends
import httpx
from auth import get_async_session
from testdata import *
from exec import CustomExec
from fastapi.responses import RedirectResponse
from routers import auth_router, utils_router, role_router, task_router
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(
    title="Trading App",
    version="0.1.1"
)



@app.get("/")
async def redirect_to_docs(session: AsyncSession = Depends(get_async_session)):
    return RedirectResponse("/docs")

CustomExec(app)

app.include_router(role_router)
app.include_router(auth_router)
app.include_router(utils_router)
app.include_router(task_router)