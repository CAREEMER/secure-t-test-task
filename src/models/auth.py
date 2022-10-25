from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from models.base import Base


class Session(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
