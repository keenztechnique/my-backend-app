from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import database
import models
import schemas
import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Comments"]
)

@router.post("/{post_id}/comments", response_model=schemas.CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # Проверяем, существует ли пост
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    new_comment = models.Comment(
        text=comment.text,
        user_id=current_user.id,
        post_id=post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/{post_id}/comments", response_model=list[schemas.CommentResponse])
def get_comments(post_id: int, db: Session = Depends(database.get_db)):
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    return comments