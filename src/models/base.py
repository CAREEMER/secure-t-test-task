import datetime
import uuid as uuid_pkg

from sqlmodel import Field, SQLModel


class ModelBase(SQLModel):
    uuid: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now, nullable=False)
