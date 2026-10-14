from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base 

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    registered_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="owner", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))

    # Связи для удобного доступа к данным
    user = relationship("User")
    post = relationship("Post")

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='unique_post_like'),
    )

    user = relationship("User")
    post = relationship("Post")