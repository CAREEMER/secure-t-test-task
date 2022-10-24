from fastapi import Depends, HTTPException
from sqlalchemy import select
from starlette import status

from core.db import get_session
from models.post import Comment, CommentThread


async def _get_parent_comment(parent_comment_id: str | None = None, session=Depends(get_session)) -> Comment | None:
    if not parent_comment_id:
        return

    parent_comment_query = select(Comment).where(Comment.id == parent_comment_id)
    parent_comment = (await session.execute(parent_comment_query)).scalar_one_or_none()

    if not parent_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent comment not found.")

    return parent_comment


async def get_or_create_thread(
    parent_comment: Comment | None = Depends(_get_parent_comment),
    parent_post_id: str | None = None,
    session=Depends(get_session),
) -> CommentThread:
    if (not (parent_comment or parent_post_id)) or (parent_comment and parent_post_id):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Provide only parent_post_id or parent_comment_id url parameter.",
        )

    if parent_post_id:
        comment_thread = CommentThread(post_id=parent_post_id)
        session.add(comment_thread)
        await session.commit()
        await session.refresh(comment_thread)
        return comment_thread

    else:
        """
        1. Check if parent_comment is last comment in thread
            is_last = True:
                2. Get thread_id parent comment attached to
                3. Return this thread

            is_last = False:
                2. Create thread with comment_id of parent_comment
                3. Return this thread
        """

        #  Check if parent_comment is last comment in thread

        last_comment_in_thread_query = (
            select(Comment)
            .where(Comment.attached_to_thread_id == parent_comment.attached_to_thread_id)
            .order_by(Comment.time_created.desc())
            .limit(1)
        )
        last_comment_in_thread = (await session.execute(last_comment_in_thread_query)).scalar()

        if parent_comment.id == last_comment_in_thread.id:
            thread_query = select(CommentThread).where(CommentThread.id == parent_comment.attached_to_thread_id)
            return (await session.execute(thread_query)).scalar()

        thread = CommentThread(comment_id=parent_comment.id)
        session.add(thread)
        await session.commit()
        await session.refresh(thread)
        return thread


async def get_thread_or_404(thread_id: str, session=Depends(get_session)) -> CommentThread:
    thread_query = select(CommentThread).where(CommentThread.id == thread_id)
    thread = (await session.execute(thread_query)).scalar()

    if not thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found.")

    return thread
