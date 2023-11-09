from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from .task_router import get_all_tasks

page_router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)

templates = Jinja2Templates(directory="templates")

@page_router.get("/base")
def get_base_page(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@page_router.get("/search/{operation_type}")
def get_search_page(request: Request, tasks=Depends(get_all_tasks)):
    print(tasks)
    return templates.TemplateResponse("search.html", {"request": request, "tasks": tasks})

@page_router.get("/chat")
def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})
