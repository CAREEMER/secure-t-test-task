from fastapi import APIRouter, Depends
from sqlalchemy import select

from api.deps.post import get_post_or_404
from core.db import get_session
from models.post import CommentThread, Post

router = APIRouter(prefix="/thread", tags=["thread"])


@router.post("/")
async def list_threads(
    post: Post = Depends(get_post_or_404), offset: int = 0, limit: int = 10, session=Depends(get_session)
):
    primary_thread_query = (
        select(CommentThread)
        .where(CommentThread.post_id == post.id)
        .order_by(CommentThread.time_created.desc())
        .offset(offset)
        .limit(limit)
    )
    threads_attached_to_post = (await session.execute(primary_thread_query)).scalars().all()

    return threads_attached_to_post
