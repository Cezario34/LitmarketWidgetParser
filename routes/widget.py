from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import select, distinct, func

from database.config import SessionLocal, Base   # ← отсюда
from utils.db_writer import BookPosition               # когда создашь модель
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER


templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/parser_widget",
    tags=["parser_widget"],
)

def parse_views(value: str) -> int:
    """Превращает '7k', '214k', '1.5m' в число"""
    if not value:
        return 0
    value = value.lower().strip().replace(",", ".")
    try:
        if value.endswith("k"):
            return int(float(value[:-1]) * 1000)
        if value.endswith("m"):
            return int(float(value[:-1]) * 1_000_000)
        return int(float(value))
    except ValueError:
        return 0


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
    book_title: Optional[str] = Query(None),
    day: Optional[str] = Query(None),
    position: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    if not request.session.get("user"):
        return RedirectResponse("/login", status_code=HTTP_303_SEE_OTHER)
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
    query = (
        select(BookPosition)
        .order_by(
            func.strftime('%Y-%m-%d %H', BookPosition.created_at).desc(),
            # сначала новый час
            BookPosition.position.asc()  # внутри часа по позиции
            )
    )
    if genre:
        query = query.where(BookPosition.genre == genre)
    if day:
        query = query.where(BookPosition.day == day)
    if position_filter:
        query = query.where(BookPosition.position == position)
    if author:
        query = query.where(BookPosition.author.ilike(f"%{author}%"))
    if book_title:
        query = query.where(BookPosition.book_title.ilike(f"%{book_title}%"))

    result = session.execute(query.limit(100))
    books = result.scalars().all()

    for book in books:
        prev = session.execute(
            select(BookPosition)
            .where(BookPosition.book_title == book.book_title)
            .where(BookPosition.created_at < book.created_at)
            .order_by(BookPosition.created_at.desc())
            .limit(1)
        ).scalar_one_or_none()

        if prev:
            book.library_delta = book.library - prev.library
            book.views_delta = parse_views(book.views) - parse_views(prev.views)
            book.likes_delta = book.likes - prev.likes
        else:
            book.library_delta = None
            book.likes_delta = None
            book.views_delta = None

    return templates.TemplateResponse(
        request,
        "book.html",
        {
            "request": request,
            "books": books,
            "genres": genres,
            "book_title": book_title,
            "genre": genre,
            "day": day,
            "author": author,
            "position": position,
        }
    )