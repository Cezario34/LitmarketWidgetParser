from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import select, distinct

from database.config import SessionLocal, Base   # ← отсюда
from utils.db_writer import BookPosition               # когда создашь модель

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/parser_widget",
    tags=["parser_widget"],
)


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/", response_class=HTMLResponse)
def get_books_page(
    request: Request,
    genre: Optional[str] = Query(None),
    day: Optional[str] = Query(None),
    position: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    # Получаем список всех существующих жанров
    genres_result = session.execute(
        select(distinct(BookPosition.genre)).order_by(BookPosition.genre)
    )
    genres = [g[0] for g in genres_result.all()]
    position_filter = None
    if position and position.strip().isdigit():
        position_filter = int(position)
    # Основной запрос
    query = (
        select(BookPosition)
        .order_by(
            BookPosition.created_at.desc(),  # сначала новые записи
            BookPosition.position.asc()  # внутри дня — по позиции от 1 и выше
        )
    )
    if genre:
        query = query.where(BookPosition.genre == genre)
    if day:
        query = query.where(BookPosition.day == day)
    if position_filter:
        query = query.where(BookPosition.position == position)

    result = session.execute(query.limit(100))
    books = result.scalars().all()

    return templates.TemplateResponse(
        request,
        "book.html",
        {
            "request": request,
            "books": books,
            "genres": genres,          # ← список жанров
            "genre": genre,
            "day": day,
            "position": position,
        }
    )