from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from starlette import status

from api.services.auth import auth_user
from api.utils import check_password, hash_password
from core.db import get_session
from models.auth import Session
from models.post import Post
from models.user import User
from serializers.post import PostCreate
from serializers.user import UserCreate

router = APIRouter(prefix="/comment")


@router.post("/")
async def create_post(post_data: PostCreate, user: User = Depends(auth_user), session=Depends(get_session)) -> Post:
    post = Post(text=post_data.text, author_uuid=user.uuid)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post
