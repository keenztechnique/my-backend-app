from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
# Импортируем Base из файла database, а не обращаемся к database как к модулю для наследования
from database import Base 

class User(Base):  # Наследуемся напрямую от Base
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    registered_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")


class Post(Base):  # Наследуемся напрямую от Base
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")