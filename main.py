from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import database

# Создаем таблицы в базе данных при запуске
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Эндпоинт для создания пользователя в базе данных (POST-запрос)
@app.post("/users/")
def create_user(username: str, db: Session = Depends(database.get_db)):
    # Проверяем, нет ли уже такого пользователя
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Создаем нового пользователя через SQLAlchemy модель
    new_user = models.User(username=username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"id": new_user.id, "username": new_user.username, "status": "created"}

# Эндпоинт для получения списка всех пользователей из базы
@app.get("/users/")
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users