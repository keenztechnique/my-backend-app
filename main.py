from fastapi import FastAPI

# Создаем экземпляр приложения
app = FastAPI()

# Создаем наш первый GET-эндпоинт по адресу /
@app.get("/")
def read_root():
    return {"message": "Привет, мир! Мой бэкенд на FastAPI работает!"}

# Создаем еще один эндпоинт для примера с параметром
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id, "status": "active"}