from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Для старта используем локальную SQLite базу данных (она создаст файл sql_app.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# Движок базы данных
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Фабрика сессий для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для наших моделей
Base = declarative_base()

# Зависимость (Dependency) для получения сессии БД в эндпоинтах
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()