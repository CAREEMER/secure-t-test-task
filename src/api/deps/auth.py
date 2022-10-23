from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import selectinload
from sqlmodel import select
from starlette import status

from core.db import get_session
from models.auth import Session
from models.user import User

session_header = APIKeyHeader(name="Authorization")


def escape_auth_header(header_value: str) -> str:
    match header_value.split(" "):
        case "Token", key:
            return key

    raise HTTPException(
        status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Provide 'Authorization: Token <key>' header."
    )


async def auth_user(session=Depends(get_session), authorization: str = Depends(session_header)) -> User:
    token = escape_auth_header(authorization)
    session_query = select(Session, User).where(Session.key == token).join(User, isouter=True)

    result = (await session.execute(session_query)).one()
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    _session_o, user = result
    return user


async def auth_user_and_get_token(session=Depends(get_session), authorization: str = Depends(session_header)) -> Session:
    token = escape_auth_header(authorization)
    session_query = select(Session).where(Session.key == token)

    session = (await session.execute(session_query)).scalar()
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return session
