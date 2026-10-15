from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import database
import models
import schemas
import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Comments"]
)

@router.post("/{post_id}/comments", response_model=schemas.CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # Проверяем, существует ли пост
    post_query = select(models.Post).where(models.Post.id == post_id)
    post_result = await db.execute(post_query)
    if not post_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    new_comment = models.Comment(
        text=comment.text,
        user_id=current_user.id,
        post_id=post_id
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment

@router.get("/{post_id}/comments", response_model=list[schemas.CommentResponse])
async def get_comments(
    post_id: int,
    db: AsyncSession = Depends(database.get_db),
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0)
):
    # Проверяем, существует ли пост
    post_query = select(models.Post).where(models.Post.id == post_id)
    post_result = await db.execute(post_query)
    if not post_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Пагинация в стиле 2.0
    comments_query = (
        select(models.Comment)
        .where(models.Comment.post_id == post_id)
        .offset(skip)
        .limit(limit)
    )
    comments_result = await db.execute(comments_query)
    return comments_result.scalars().all()