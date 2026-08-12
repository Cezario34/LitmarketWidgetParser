from app.models.bookinfo import BookPosition
from datetime import date
from sqlalchemy.orm import  Session
from app.database.config import engine
import logging

def write_to_db(data: dict, genre: str, logger: logging.Logger | None = None) -> None:
    if logger:
        logger.info(f"Writing data to database (genre: {genre})...")

    today = date.today()
    objects = []

    for position, (title, values) in enumerate(data.items(), start=1):
        obj = BookPosition(
            book_title=title,
            day=today,
            position=position,
            genre=genre,
            author=values.get("author", ""),
            library=values.get("library", 0),
            likes=values.get("likes", 0),
            views=str(values.get("views", "")),
        )
        objects.append(obj)

    if not objects:
        if logger:
            logger.warning("Нет данных для записи")
        return

    with Session(engine) as session:
        session.add_all(objects)
        session.commit()

    if logger:
        logger.info(f"Успешно записано {len(objects)} книг за {today} (жанр: {genre})")