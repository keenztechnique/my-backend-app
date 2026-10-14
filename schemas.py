from pydantic import BaseModel, Field
from datetime import datetime

class UserCreate(BaseModel):
    # Добавляем ограничение: имя должно быть не короче 3 символов
    username: str = Field(..., min_length=3, description="Имя пользователя должно содержать минимум 3 символа")
    password: str  # <--- Добавляем поле для пароля при регистрации
    
class UserResponse(BaseModel):
    id: int
    username: str
    registered_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: str

# Схема для создания поста
class PostCreate(BaseModel):
    title: str
    content: str

# Схема для отображения поста клиенту
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class CommentCreate(BaseModel):
    text: str

class CommentResponse(BaseModel):
    id: int
    text: str
    user_id: int
    post_id: int

    class Config:
        from_attributes = True

class LikeResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True