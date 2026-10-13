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
@app.get("/users/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users

# Эндпоинт для получения конкретного пользователя по ID
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user

# Эндпоинт для удаления пользователя по ID
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    # Ищем пользователя в базе
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    # Если пользователя нет — возвращаем 404
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Удаляем пользователя и фиксируем изменения в базе
    db.delete(user)
    db.commit()
    
    return {"message": "User deleted successfully"}

# Эндпоинт для обновления данных пользователя по ID
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    # 1. Ищем пользователя в базе
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    # 2. Если не нашли — возвращаем 404
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    # 3. Обновляем поле username данными, которые прислал клиент
    db_user.username = user_update.username
    
    # 4. Сохраняем изменения в базе
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Эндпоинт для создания поста конкретным пользователем
@app.post("/users/{user_id}/posts/", response_model=schemas.PostResponse)
def create_post_for_user(user_id: int, post: schemas.PostCreate, db: Session = Depends(database.get_db)):
    # Проверяем, существует ли пользователь
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Создаем объект поста, привязывая его к user_id
    db_post = models.Post(**post.dict(), user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Эндпоинт для получения всех постов
@app.get("/posts/", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(database.get_db)):
    return db.query(models.Post).all()