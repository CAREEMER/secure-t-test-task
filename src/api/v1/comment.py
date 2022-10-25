from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select, update
from sqlalchemy.orm import immediateload, joinedload, lazyload, selectinload
from sqlalchemy_utils import Ltree
from starlette import status

from api.deps.auth import auth_user
from api.deps.comment import get_comment_or_404, get_parent_comment_or_404
from api.deps.post import get_post_or_404
from api.utils import escape_ltree_path
from core.db import get_session, get_sync_session
from models.post import Comment, Post
from models.user import User
from serializers.comment import CommentCreate, CommentList, CommentUpdate

router = APIRouter(prefix="/comment", tags=["comment"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    parent_comment: Comment | None = Depends(get_parent_comment_or_404),
    user: User = Depends(auth_user),
    db_session=Depends(get_session),
):
    comment = Comment(**comment_data.dict(), id=uuid4(), author_id=user.id)

    if not parent_comment:
        ltree_node_path = escape_ltree_path(f"{comment.id}")
    else:
        ltree_node_path = escape_ltree_path(f"{parent_comment.node_path}.{comment.id}")

    comment.node_path = Ltree(ltree_node_path)

    db_session.add(comment)
    await db_session.commit()
    await db_session.refresh(comment)

    return comment


@router.patch("/{comment_id}/")
async def update_comment(
    comment_data: CommentUpdate,
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
async def list_comment(post: Post = Depends(get_post_or_404), db_session=Depends(get_sync_session)):
    comments_query = select(Comment).where(Comment.post_id == post.id).where(func.nlevel(Comment.node_path) == 1)
    comments = (db_session.execute(comments_query)).scalars().all()

    return [CommentList(**comment.dict(), children=getattr(comment, "children", [])) for comment in comments]


@router.delete("/{comment_id}/", status_code=status.HTTP_202_ACCEPTED)
async def delete_comment(
    comment: Comment = Depends(get_comment_or_404),
    user: User = Depends(auth_user),
    db_session=Depends(get_session),
):
    if comment.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission for editing this comment.")

    comment.deleted = True
    comment.text = "[DELETED]"

    await db_session.commit()
