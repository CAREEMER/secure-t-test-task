from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.deps.auth import auth_user
from api.deps.post import get_post_or_404
from core.db import get_session
from models.post import Post
from models.user import User
from serializers.post import PostCreate, PostRetrieve

router = APIRouter(prefix="/post", tags=["post"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostRetrieve)
async def create_post(
    post_data: PostCreate, user: User = Depends(auth_user), db_session=Depends(get_session)
) -> PostRetrieve:
    post = Post(text=post_data.text, author_id=user.id)
    db_session.add(post)
    await db_session.commit()
    await db_session.refresh(post)
    return PostRetrieve(**post.dict())


@router.get("/{post_id}/", response_model=PostRetrieve)
async def get_post(post: Post = Depends(get_post_or_404)) -> PostRetrieve:
    return PostRetrieve(**post.dict())


@router.patch("/{post_id}/", response_model=PostRetrieve)
async def update_post(
    post_data: PostCreate,
    post: Post = Depends(get_post_or_404),
    user: User = Depends(auth_user),
    db_session=Depends(get_session),
) -> PostRetrieve:
    if post.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission for editing this comment.")

    post.text = post_data.text
    await db_session.commit()
    await db_session.refresh(post)

    return PostRetrieve(**post.dict())


@router.delete("/{post_id}/", status_code=status.HTTP_202_ACCEPTED)
async def delete_post(
    post: Post = Depends(get_post_or_404), user: User = Depends(auth_user), db_session=Depends(get_session)
):
    if post.author_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission for editing this comment.")

    post.deleted = True
    await db_session.commit()
