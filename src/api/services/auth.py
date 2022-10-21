from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException
from starlette import status
from sqlmodel import select
from core.db import get_session
from models.user import User
from models.auth import Session


session_header = APIKeyHeader(name="Authorization")


def escape_auth_header(header_value: str) -> str:
    match header_value.split(" "):
        case "Token", key:
            return key

    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Provide 'Authorization: Token <key>' header.")


async def auth_user(
    session=Depends(get_session),
    authorization: str = Depends(session_header)
) -> User:
    token = escape_auth_header(authorization)
    session_query = select(Session, User).where(Session.key == token).join(User, isouter=True)

    results = (await session.execute(session_query)).all()
    if not results:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return results[0][1]
