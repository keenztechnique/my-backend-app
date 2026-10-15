from fastapi import FastAPI
from database import engine, Base
import models  
# Чистые и понятные импорты без дублирования
from routers import auth, users, posts, comments, likes

app = FastAPI(
    title="My Professional Backend API",
    version="2.0.0"
)

# Подключаем ВСЕ роутеры по очереди
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)     # <-- Убедись, что эта строка активна и не закомментирована
app.include_router(comments.router)
app.include_router(likes.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the professional FastAPI backend!"}