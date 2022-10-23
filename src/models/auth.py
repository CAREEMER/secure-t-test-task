from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from models.user import User


class Session(SQLModel, table=True):
    user_uuid: UUID = Field(nullable=False, foreign_key="user.uuid")
    user: User = Relationship(back_populates="sessions")
    key: UUID = Field(default_factory=uuid4, nullable=False, index=True, primary_key=True)
