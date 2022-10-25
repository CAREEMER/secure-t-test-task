from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from starlette import status

from api.deps.auth import auth_user_and_get_token
from api.utils import check_password, hash_password
from core.db import get_session
from models.auth import Session
from models.user import User
from serializers.session import SessionRetrieve
from serializers.user import UserCreate, UserRetrieve

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register/", status_code=status.HTTP_201_CREATED, response_model=UserRetrieve)
async def register_user(user_data: UserCreate, db_session=Depends(get_session)) -> UserRetrieve:
    user = User(username=user_data.username, password=hash_password(user_data.password))
    db_session.add(user)
    try:
        await db_session.commit()
    except IntegrityError as _:  # NOQA: F841
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with that username already exists.")
    await db_session.refresh(user)

    return UserRetrieve(**user.dict())


@router.post("/login/", status_code=status.HTTP_201_CREATED, response_model=SessionRetrieve)
async def login(user_data: UserCreate, db_session=Depends(get_session)) -> SessionRetrieve:
    user_query = select(User).where(User.username == user_data.username)
    user = (await db_session.execute(user_query)).scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong username or password.")

    if check_password(user_data.password, user.password):
        auth_session = Session(user_id=user.id)
        db_session.add(auth_session)
        await db_session.commit()
        await db_session.refresh(auth_session)

        return SessionRetrieve(token=auth_session.id)

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong username or password.")


@router.post("/logout/", status_code=status.HTTP_202_ACCEPTED)
async def logout(session=Depends(auth_user_and_get_token), db_session=Depends(get_session)) -> None:
    delete_session_query = delete(Session).where(Session.id == session.id)
    await db_session.execute(delete_session_query)
    await db_session.commit()
    return
