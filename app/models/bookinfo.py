from datetime import date, datetime
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine, String, Date, Integer, select, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
import logging
from app.database.config import engine, Base


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
    Base.metadata.create_all(engine)
    msg = f"Database initialized."
    if logger is not None:
        logger.info(msg)
    else:
        print(msg)

