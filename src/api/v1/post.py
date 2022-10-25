from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from starlette import status

from api.deps.auth import auth_user
from api.deps.post import get_post_or_404
from core.db import get_session
from models.post import Post, PostUpvote
from models.user import User
from serializers.post import PostCreate, PostRetrieve

router = APIRouter(prefix="/post", tags=["post"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate, user: User = Depends(auth_user), db_session=Depends(get_session)) -> Post:
    post = Post(text=post_data.text, author_id=user.id)
    db_session.add(post)
    await db_session.commit()
    await db_session.refresh(post)
    return post


@router.get("/{post_id}/")
async def get_post(post: Post = Depends(get_post_or_404)) -> PostRetrieve:
    return post


@router.patch("/{post_id}/")
async def update_post(
    post_data: PostCreate,
    post: Post = Depends(get_post_or_404),
    user: User = Depends(auth_user),
    db_session=Depends(get_session),
):
    if post.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission for editing this comment.")

    post.text = post_data.text
    await db_session.commit()
    await db_session.refresh(post)

    return post


@router.delete("/{post_id}/", status_code=status.HTTP_202_ACCEPTED)
async def delete_post(
    post: Post = Depends(get_post_or_404), user: User = Depends(auth_user), db_session=Depends(get_session)
):
    if post.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission for editing this comment.")

    post.deleted = True
    await db_session.commit()
