from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from starlette import status

from api.deps.auth import auth_user
from api.deps.post import get_post_or_404
from core.db import get_session
from models.post import Post, PostUpvote, Comment, CommentThread
from models.user import User
from serializers.post import PostCreate, PostRetrieve
from serializers.comment import CommentCreate

router = APIRouter(prefix="/comment", tags=["comment"])


@router.post("/")
async def create_comment(comment_data: CommentCreate, user: User = Depends(auth_user), session=Depends(get_session)):
    comment = Comment(**comment_data.dict(), author_id=user.id)

    if comment.parent_post_id:
        comment_thread = CommentThread(post_id=comment.parent_post_id)

        session.add(comment_thread)
        await session.commit()
        await session.refresh(comment_thread)

        comment.attached_to_thread_id = comment_thread.id
        comment.index_in_thread = 0

        session.add(comment)
        await session.commit()
        await session.refresh(comment)

        return comment

    elif comment.parent_comment_id:
        parent_comment_query = select(Comment).where(Comment.id == comment.parent_comment_id)
        parent_comment = await session.execute()


    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment
