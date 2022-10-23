from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.exc import IntegrityError
from sqlmodel import delete, select
from starlette import status

from api.deps.auth import auth_user_and_get_token
from api.utils import check_password, hash_password
from core.db import get_session
from models.auth import Session
from models.user import User
from serializers.user import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register/")
async def register_user(user_data: UserCreate, db_session=Depends(get_session)) -> User:
    user = User(username=user_data.username, password=hash_password(user_data.password))
    db_session.add(user)
    try:
        await db_session.commit()
    except IntegrityError as _:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with that username already exists.")
    await db_session.refresh(user)

    return user


@router.post("/login/")
async def login(user_data: UserCreate, db_session=Depends(get_session)) -> Session:
    user_query = select(User).where(User.username == user_data.username)
    user = (await db_session.execute(user_query)).scalar()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong username or password.")

    if check_password(user_data.password, user.password):
        auth_session = Session(user_uuid=user.uuid)
        db_session.add(auth_session)
        await db_session.commit()
        await db_session.refresh(auth_session)

        return auth_session

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong username or password.")


@router.post("/logout/")
async def logout(session_o=Depends(auth_user_and_get_token), db_session=Depends(get_session)):
    delete_session_query = delete(Session).where(Session.key == session_o.key)
    await db_session.execute(delete_session_query)
    await db_session.commit()
    return Response(status_code=status.HTTP_202_ACCEPTED)
