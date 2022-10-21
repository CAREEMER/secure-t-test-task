from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, delete
from starlette import status
from core.db import get_session
from models.user import User
from models.post import Post, PostUpvote
from models.auth import Session
from serializers.user import UserCreate
from api.utils import hash_password, check_password
from api.services.auth import auth_user
from serializers.post import PostCreate
from api.services.post import get_post_or_404

router = APIRouter(prefix="/post")


@router.post("/")
async def create_post(post_data: PostCreate, user: User = Depends(auth_user), session = Depends(get_session)) -> Post:
    post = Post(text=post_data.text, author_uuid=user.uuid)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@router.post("/{post_uuid}/upvote/")
async def bump_post(user: User = Depends(auth_user), post: Post = Depends(get_post_or_404), session = Depends(get_session)) -> PostUpvote:
    upvote_query = select(PostUpvote).where(PostUpvote.user_uuid == user.uuid).where(PostUpvote.post_uuid == post.uuid)
    existing_upvote = (await session.execute(upvote_query)).scalar()

    if existing_upvote:
        delete_upvote_query = delete(PostUpvote).where(PostUpvote.uuid == existing_upvote.uuid)
        await session.execute(delete_upvote_query)

    upvote = PostUpvote(post_uuid=post.uuid, user_uuid=user.uuid, positive=True)
    session.add(upvote)
    await session.commit(upvote)
    await session.refresh(upvote)
    return upvote





@router.post("/{post_uuid}/downvote/")
async def sage_post(user: User = Depends(auth_user), post: Post = Depends(get_post_or_404), session = Depends(get_session)) -> Post:
    pass
