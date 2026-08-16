from fastapi import FastAPI
from app.routes import widget, check_book, auth
from starlette.middleware.sessions import SessionMiddleware
from config import get_settings
from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
templates = Jinja2Templates(directory="templates")



app = FastAPI(
    title="Парсер Виджетов",
    version="0.1.0",
    )
settings = get_settings()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(widget.router)
app.include_router(auth.router)
app.include_router(check_book.router)

@app.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse(request, "welcome.html")