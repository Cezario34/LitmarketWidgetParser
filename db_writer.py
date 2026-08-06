from datetime import date, datetime
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine, String, Date, Integer, select, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
import logging

DB_FILE = Path('books_tracking.db')
ENGINE = create_engine(f"sqlite:///{DB_FILE}", echo=False)

class Base(DeclarativeBase):
    pass


class BookPosition(Base):
    __tablename__ = 'book_position'


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    book_title: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    day: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    genre: Mapped[str] = mapped_column(
        String(100), nullable=False, index=True
        )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    library: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    likes: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    views: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

def init_db(logger: logging.Logger | None = None) -> None:
    Base.metadata.create_all(ENGINE)
    msg = f"Database initialized."
    if logger is not None:
        logger.info(msg)
    else:
        print(msg)

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

    with Session(ENGINE) as session:
        session.add_all(objects)
        session.commit()

    if logger:
        logger.info(f"Успешно записано {len(objects)} книг за {today} (жанр: {genre})")