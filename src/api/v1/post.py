from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import delete, func, select
from starlette import status

from api.services.auth import auth_user
from api.services.post import get_post_or_404, get_post_with_aggregations_or_404
from api.utils import check_password, hash_password
from core.db import get_session
from models.auth import Session
from models.post import Post, PostUpvote
from models.user import User
from serializers.post import PostCreate, PostRetrieve
from serializers.user import UserCreate

router = APIRouter(prefix="/post")


@router.post("/")
async def create_post(post_data: PostCreate, user: User = Depends(auth_user), session=Depends(get_session)) -> Post:
    post = Post(text=post_data.text, author_uuid=user.uuid)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@router.get("/")
async def get_post(
    post: Post = Depends(get_post_with_aggregations_or_404), session=Depends(get_session)
) -> PostRetrieve:
    # upvotes_count_query = select([func.count()]).where(PostUpvote.post_uuid == post.uuid).where(PostUpvote.positive == True).select_from(PostUpvote)
    # downvotes_count_query = select([func.count()]).where(PostUpvote.post_uuid == post.uuid).where(PostUpvote.positive == False).select_from(PostUpvote)
    #
    # upvotes_count = (await session.execute(upvotes_count_query)).scalar()
    # downvotes_count = (await session.execute(downvotes_count_query)).scalar()
    #
    # return PostRetrieve(**post.dict(), upvote_count=upvotes_count - downvotes_count)
    pass


@router.post("/{post_uuid}/upvote/")
async def bump_post(
    user: User = Depends(auth_user), post: Post = Depends(get_post_or_404), session=Depends(get_session)
) -> PostUpvote:
    upvote_query = select(PostUpvote).where(PostUpvote.user_uuid == user.uuid).where(PostUpvote.post_uuid == post.uuid)
    existing_upvote = (await session.execute(upvote_query)).scalar()

    if existing_upvote:
        if existing_upvote.positive:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Upvote already exists.")

        delete_upvote_query = delete(PostUpvote).where(PostUpvote.uuid == existing_upvote.uuid)
        await session.execute(delete_upvote_query)

    upvote = PostUpvote(post_uuid=post.uuid, user_uuid=user.uuid, positive=True)
    session.add(upvote)
    await session.commit()
    await session.refresh(upvote)
    return upvote


@router.post("/{post_uuid}/downvote/")
async def sage_post(
    user: User = Depends(auth_user), post: Post = Depends(get_post_or_404), session=Depends(get_session)
) -> PostUpvote:
    upvote_query = select(PostUpvote).where(PostUpvote.user_uuid == user.uuid).where(PostUpvote.post_uuid == post.uuid)
    existing_upvote = (await session.execute(upvote_query)).scalar()

    if existing_upvote:
        if not existing_upvote.positive:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Upvote already exists.")

        delete_upvote_query = delete(PostUpvote).where(PostUpvote.uuid == existing_upvote.uuid)
        await session.execute(delete_upvote_query)

    upvote = PostUpvote(post_uuid=post.uuid, user_uuid=user.uuid, positive=False)
    session.add(upvote)
    await session.commit()
    await session.refresh(upvote)
    return upvote
