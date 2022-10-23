from uuid import uuid4

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base


class Session(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    key = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
