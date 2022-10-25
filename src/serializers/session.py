from pydantic import UUID4, BaseModel


class SessionRetrieve(BaseModel):
    token: UUID4
