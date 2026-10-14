import sys
import os

# Добавляем корень проекта в путь поиска Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app

# Используем SQLite в памяти для тестов (быстро и изолированно)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Подменяем реальную зависимость базы данных на тестовую
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    # Создаем таблицы перед каждым тестом
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Удаляем таблицы после теста
    Base.metadata.drop_all(bind=engine)