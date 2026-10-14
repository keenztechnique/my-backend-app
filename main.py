from fastapi import FastAPI
import models
import database
from routers import users, posts, auth
from routers import auth, users, posts, comments
from routers import auth, users, posts, comments, likes

# Создаем таблицы в базе данных при запуске
#models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="My Professional Backend API",
    version="2.0.0"
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)

@app.get("/")
def root():
    return {"message": "Welcome to the professional FastAPI backend!"}