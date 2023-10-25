from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse
from fastapi import FastAPI

class CustomExec:
    app:FastAPI = None

    def __init__(self, app:FastAPI):
        self.app = app
        @app.exception_handler(ValidationException)
        async def validation_exception_handler(request: Request, exc: ValidationException):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content=jsonable_encoder({"detail": exc.errors()})
            )