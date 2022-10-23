from sqlalchemy import Column, Text

from models.base import Base


class User(Base):
    username: str = Column(Text, index=True, unique=True, nullable=False)
    password: str = Column(Text, nullable=False)
