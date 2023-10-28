from fastapi import FastAPI
from testdata import *
from exec import CustomExec
from fastapi.responses import RedirectResponse
from routers import auth_router, utils_router, role_router

app = FastAPI(
    title="Trading App",
    version="0.1.1"
)

@app.get("/")
async def redirect_to_docs():
    return RedirectResponse("/docs")

CustomExec(app)

app.include_router(role_router)
app.include_router(auth_router)
app.include_router(utils_router)