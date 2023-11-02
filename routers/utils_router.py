from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
import httpx
from auth import User
from .auth_router import current_user
from faker import Faker
import uuid
import os
from random import randint

faker = Faker("ru_RU")

utils_router = APIRouter(
    prefix="/utils",
    tags=["Utils"]
)

IMAGEDIR = "images/"
    

@utils_router.get("/test-auth")
def protected_route(user: User = Depends(current_user)):
    try:    
        return f"Hello, {user.username}"
    except Exception as ex:
            raise HTTPException(status_code=555, detail=ex)


@utils_router.get("/test")
def unprotected_route():
    try:    
        x = 10 / 0
        return f"Hello, {x}"
    except Exception as ex:
        raise HTTPException(status_code=555, detail=str(ex))

@utils_router.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()

    
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)

    return {"filename":file}

@utils_router.get("/show/")
async def read_random_file():
    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) - 1)

    path = f"{IMAGEDIR}{files[random_index]}"

    return FileResponse(path)