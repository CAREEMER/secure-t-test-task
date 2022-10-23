from fastapi import Depends, HTTPException
from sqlmodel import func, select
from starlette import status

from core.db import get_session
from models.post import Post, PostUpvote


async def get_post_or_404(post_uuid: str, session=Depends(get_session)):
    post_query = select(Post).where(Post.uuid == post_uuid)
    post = (await session.execute(post_query)).scalar()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post doesn't exist.")

    return post


async def get_post_with_aggregations_or_404(post_uuid: str, session=Depends(get_session)):
    post_query = select(Post, func.count(PostUpvote.uuid))
