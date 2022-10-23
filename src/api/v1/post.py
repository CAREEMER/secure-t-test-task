from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from starlette import status

from api.deps.auth import auth_user
from api.deps.post import get_post_or_404, get_post_with_aggregations_or_404
from core.db import get_session
from models.post import Post, PostUpvote
from models.user import User
from serializers.post import PostCreate, PostRetrieve

router = APIRouter(prefix="/post")


@router.post("/")
async def create_post(post_data: PostCreate, user: User = Depends(auth_user), db_session=Depends(get_session)) -> Post:
    post = Post(text=post_data.text, author_id=user.id)
    db_session.add(post)
    await db_session.commit()
    await db_session.refresh(post)
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
    user: User = Depends(auth_user), post: Post = Depends(get_post_or_404), db_session=Depends(get_session)
) -> PostUpvote:
    upvote_query = select(PostUpvote).where(PostUpvote.user_id == user.id).where(PostUpvote.post_id == post.id)
    existing_upvote = (await db_session.execute(upvote_query)).scalar()

    if existing_upvote:
        if existing_upvote.positive:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Upvote already exists.")

        delete_upvote_query = delete(PostUpvote).where(PostUpvote.id == existing_upvote.id)
        await db_session.execute(delete_upvote_query)

    upvote = PostUpvote(post_id=post.id, user_id=user.id, positive=True)
    db_session.add(upvote)
    await db_session.commit()
    await db_session.refresh(upvote)
    return upvote


@router.post("/{post_uuid}/downvote/")
async def sage_post(
    user: User = Depends(auth_user), post: Post = Depends(get_post_or_404), session=Depends(get_session)
) -> PostUpvote:
    upvote_query = select(PostUpvote).where(PostUpvote.user_id == user.id).where(PostUpvote.post_id == post.id)
    existing_upvote = (await session.execute(upvote_query)).scalar()

    if existing_upvote:
        if not existing_upvote.positive:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Upvote already exists.")

        delete_upvote_query = delete(PostUpvote).where(PostUpvote.id == existing_upvote.id)
        await session.execute(delete_upvote_query)

    upvote = PostUpvote(post_id=post.id, user_id=user.id, positive=False)
    session.add(upvote)
    await session.commit()
    await session.refresh(upvote)
    return upvote
