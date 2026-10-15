import bcrypt

def hash_password(password: str) -> str:
    # Переводим пароль в байты, обрезая до 72 байт ради безопасности bcrypt
    pwd_bytes = password.encode('utf-8')[:72]
    # Генерируем соль и хэшируем
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    # Возвращаем строкой для сохранения в базу данных
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')[:72]
    # Проверяем соответствие
    return bcrypt.checkpw(pwd_bytes, hashed_password.encode('utf-8'))