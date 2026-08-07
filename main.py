from fastapi import FastAPI
from routes.auth import router as auth_router
from routes import widget
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from config import get_settings



app = FastAPI(
    title="Парсер Виджетов",
    version="0.1.0",
    )
settings = get_settings()

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(widget.router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Парсер виджетов"}