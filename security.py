from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from config import settings  # <--- Импортируем наши настройки

# Используем данные из конфига вместо хардкода
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    # Ограничиваем пароль 72 байтами для безопасности bcrypt
    pwd_bytes = password.encode('utf-8')[:72]
    return pwd_context.hash(pwd_bytes)

def verify_password(plain_password, hashed_password):
    pwd_bytes = plain_password.encode('utf-8')[:72]
    return pwd_context.verify(pwd_bytes, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt