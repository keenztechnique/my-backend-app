from pydantic import BaseModel
from datetime import datetime

# Схема, которую мы ждем ОТ клиента при создании пользователя
class UserCreate(BaseModel):
    username: str

# Схема, которую мы возвращаем КЛИЕНТУ (уже содержит ID и дату из базы)
class UserResponse(BaseModel):
    id: int
    username: str
    registered_at: datetime

    class Config:
        # Эта настройка говорит Pydantic: «Умей читать данные, даже если они приходят из ORM-моделей SQLAlchemy, а не просто из словарей»
        from_attributes = True