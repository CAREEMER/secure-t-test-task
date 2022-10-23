from fastapi import APIRouter, Depends

from api.deps.auth import auth_user
from core.db import get_session
from models.post import Post
from models.user import User
from serializers.post import PostCreate

router = APIRouter(prefix="/comment")


@router.post("/")
async def create_post(post_data: PostCreate, user: User = Depends(auth_user), session=Depends(get_session)) -> Post:
    post = Post(text=post_data.text, author_uuid=user.uuid)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post
