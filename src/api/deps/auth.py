from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy import select
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


async def auth_user(db_session=Depends(get_session), authorization: str = Depends(session_header)) -> User:
    token = escape_auth_header(authorization)
    auth_session_query = select(Session, User).where(Session.id == token).join(User, isouter=True)

    result = (await db_session.execute(auth_session_query)).all()
    if not result:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    _auth_session, user = result[0]
    return user


async def auth_user_and_get_token(
    db_session=Depends(get_session), authorization: str = Depends(session_header)
) -> Session:
    token = escape_auth_header(authorization)
    auth_session_query = select(Session).where(Session.id == token)

    auth_session = (await db_session.execute(auth_session_query)).scalar()
    if not auth_session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return auth_session
