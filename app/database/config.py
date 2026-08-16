from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase # New
from pathlib import  Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Строка подключения для SQLite
DATABASE_URL = f"sqlite:///{BASE_DIR / 'books_tracking.db'}"
# Создаём Engine
engine = create_engine(DATABASE_URL)

# Настраиваем фабрику сеансов
SessionLocal = sessionmaker(bind=engine)


# Определяем базовый класс для моделей
class Base(DeclarativeBase):  # New
    pass