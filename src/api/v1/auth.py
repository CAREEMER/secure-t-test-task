from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from starlette import status

from api.utils import check_password, hash_password
from core.db import get_session
from models.auth import Session
from models.user import User
from serializers.user import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register/")
async def register_user(user_data: UserCreate, session=Depends(get_session)) -> User:
    user = User(username=user_data.username, password=hash_password(user_data.password))
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as _:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with that username already exists.")
    await session.refresh(user)

    return user


@router.post("/login/")
async def login(user_data: UserCreate, session=Depends(get_session)) -> Session:
    user_query = select(User).where(User.username == user_data.username)
    user = (await session.execute(user_query)).scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong username or password.")

    if check_password(user_data.password, user.password):
        session_o = Session(user_uuid=user.uuid)
        session.add(session_o)
        await session.commit()
        await session.refresh(session_o)

        return session_o

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong username or password.")
