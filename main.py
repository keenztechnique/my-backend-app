from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import database
import schemas

# Создаем таблицы в базе данных при запуске
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Эндпоинт для создания пользователя
# Обратите внимание: вместо `username: str` мы принимаем `user: schemas.UserCreate`
# А в ответе указываем `response_model=schemas.UserResponse`
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    # Проверяем, нет ли уже такого пользователя (обращаемся к .username у pydantic-объекта)
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Создаем нового пользователя, передавая данные из pydantic-схемы
    new_user = models.User(username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# Эндпоинт для получения списка всех пользователей
# Возвращает список объектов, соответствующих схеме UserResponse
@app.get("/users/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users