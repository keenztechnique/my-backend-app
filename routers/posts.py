# routers/posts.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, update
import database
import models
import schemas
from oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]  # Этот тег создаст долгожданную секцию в Swagger UI
)

@router.get("/", response_model=list[schemas.PostResponse])
async def get_posts(
    db: AsyncSession = Depends(database.get_db),
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    search: Optional[str] = Query(None)
):
    stmt = select(models.Post)
    if search:
        stmt = stmt.where(models.Post.title.ilike(f"%{search}%"))
    
    stmt = stmt.offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: schemas.PostCreate, 
    db: AsyncSession = Depends(database.get_db), 
    current_user: models.User = Depends(get_current_user)
):
    new_post = models.Post(**post.model_dump(), user_id=current_user.id)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

@router.get("/me", response_model=list[schemas.PostResponse])
async def get_my_posts(
    db: AsyncSession = Depends(database.get_db), 
    current_user: models.User = Depends(get_current_user)
):
    stmt = select(models.Post).where(models.Post.user_id == current_user.id)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{post_id}", response_model=schemas.PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(database.get_db)):
    stmt = select(models.Post).where(models.Post.id == post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    return post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int, 
    db: AsyncSession = Depends(database.get_db), 
    current_user: models.User = Depends(get_current_user)
):
    stmt = select(models.Post).where(models.Post.id == post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
        
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
        
    delete_stmt = delete(models.Post).where(models.Post.id == post_id)
    await db.execute(delete_stmt)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}", response_model=schemas.PostResponse)
async def update_post(
    post_id: int, 
    updated_post: schemas.PostCreate, 
    db: AsyncSession = Depends(database.get_db), 
    current_user: models.User = Depends(get_current_user)
):
    stmt = select(models.Post).where(models.Post.id == post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
        
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action"
        )
        
    update_stmt = (
        update(models.Post)
        .where(models.Post.id == post_id)
        .values(**updated_post.model_dump())
    )
    await db.execute(update_stmt)
    await db.commit()
    
    await db.refresh(post)
    return post