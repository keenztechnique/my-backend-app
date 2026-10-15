from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import database
import models
import schemas
import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Likes"]
)

@router.post("/{post_id}/like", response_model=schemas.LikeResponse)
async def toggle_like(
    post_id: int,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user)
):
    # Проверяем пост
    post_query = select(models.Post).where(models.Post.id == post_id)
    post_result = await db.execute(post_query)
    if not post_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Ищем существующий лайк
    like_query = select(models.Like).where(
        models.Like.post_id == post_id,
        models.Like.user_id == current_user.id
    )
    like_result = await db.execute(like_query)
    existing_like = like_result.scalar_one_or_none()

    if existing_like:
        await db.delete(existing_like)
        await db.commit()
        return {"message": "Like removed successfully"}
    else:
        new_like = models.Like(user_id=current_user.id, post_id=post_id)
        db.add(new_like)
        await db.commit()
        return {"message": "Post liked successfully"}