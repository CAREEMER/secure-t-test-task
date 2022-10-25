from fastapi import Depends, HTTPException
from sqlalchemy import select
from starlette import status

from core.db import get_session
from models.post import Post


async def get_post_or_404(post_id: str, session=Depends(get_session)):
    post_query = select(Post).where(Post.id == post_id).where(Post.deleted == False)
    post = (await session.execute(post_query)).scalar()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post doesn't exist.")

    return post
