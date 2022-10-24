from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from starlette import status

from api.deps.auth import auth_user
from api.deps.thread import get_or_create_thread, get_thread_or_404
from api.deps.comment import get_comment_or_404
from core.db import get_session
from models.post import Comment, CommentThread
from models.user import User
from serializers.comment import CommentCreate, CommentList

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


@router.patch("/{comment_id}/")
async def update_comment(
    comment_data: CommentCreate,
    comment: Comment = Depends(get_comment_or_404),
    user: User = Depends(auth_user),
    db_session=Depends(get_session),
):
    if comment.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission for editing this comment.")

    comment.text = comment_data.text
    await db_session.commit()
    await db_session.refresh(comment)

    return comment



@router.get("/")
async def list_comment(
    thread: CommentThread = Depends(get_thread_or_404), offset: int = 0, limit: int = 10, session=Depends(get_session)
):
    comment_query = (
        select(Comment)
        .where(Comment.attached_to_thread_id == thread.id)
        .order_by(Comment.time_created)
        .offset(offset)
        .limit(limit)
    )
    comments = (await session.execute(comment_query)).scalars().all()
    _comment_ids = [_comment.id for _comment in comments]

    comment_thread_query = select(CommentThread.id, CommentThread.comment_id).where(
        CommentThread.comment_id.in_(_comment_ids)
    )
    comment_threads = (await session.execute(comment_thread_query)).all()

    #  pizdec... zato vsego lish' 2 db queries :)
    #  LEFT OUTER JOIN s paginaciei ne poluchilos' podruzhit' :)
    comment_id_thread_ids_map = {}
    for th in comment_threads:
        if not comment_id_thread_ids_map.get(th[1], None):
            comment_id_thread_ids_map[th[1]] = [th[0]]
        else:
            comment_id_thread_ids_map[th[1]].append(th[0])

    serialized_comments = []
    for comment in comments:
        data = comment.dict()
        data["threads_attached_to_comment"] = comment_id_thread_ids_map.get(comment.id, [])
        serialized_comments.append(CommentList(**data))

    return serialized_comments
