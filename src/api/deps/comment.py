from fastapi import Depends, HTTPException
from sqlalchemy import select
from starlette import status

from core.db import get_session
from models.post import Comment


async def get_comment_or_404(comment_id: str, db_session=Depends(get_session)):
    comment_query = select(Comment).where(Comment.id == comment_id)
    comment = (await db_session.execute(comment_query)).scalar()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found.")

    return comment
