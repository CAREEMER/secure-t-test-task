from fastapi import APIRouter, Depends
from sqlalchemy import select

from api.deps.auth import auth_user
from api.deps.thread import get_or_create_thread, get_thread_or_404
from core.db import get_session
from models.post import Comment, CommentThread
from models.user import User
from serializers.comment import CommentCreate

router = APIRouter(prefix="/comment", tags=["comment"])


@router.post("/")
async def create_comment(
    comment_data: CommentCreate,
    user: User = Depends(auth_user),
    thread=Depends(get_or_create_thread),
    session=Depends(get_session),
):
    comment = Comment(**comment_data.dict(), attached_to_thread_id=thread.id, author_id=user.id)
    session.add(comment)
    await session.commit()
    await session.refresh(comment)

    return comment


@router.get("/")
async def list_comment(
    thread: CommentThread = Depends(get_thread_or_404), offset: int = 0, limit: int = 10, session=Depends(get_session)
):
    comment_query = (
        select(Comment)
        .where(Comment.attached_to_thread_id == thread.id)
        .order_by(Comment.time_created.asc())
        .offset(offset)
        .limit(limit)
    )
    comments = (await session.execute(comment_query)).scalars().all()

    return comments
