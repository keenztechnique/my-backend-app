from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database
import models
import schemas
import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Likes"]
)

@router.post("/{post_id}/like", response_model=schemas.LikeResponse)
def toggle_like(
    post_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # Проверяем, существует ли пост
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Ищем существующий лайк от этого пользователя
    existing_like = db.query(models.Like).filter(
        models.Like.post_id == post_id,
        models.Like.user_id == current_user.id
    ).first()

    if existing_like:
        # Если лайк уже есть — удаляем (снимаем лайк)
        db.delete(existing_like)
        db.commit()
        return {"message": "Like removed successfully"}
    else:
        # Если лайка нет — ставим
        new_like = models.Like(user_id=current_user.id, post_id=post_id)
        db.add(new_like)
        db.commit()
        return {"message": "Post liked successfully"}