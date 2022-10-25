from sqlalchemy import Boolean, Column, ForeignKey, Index, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import foreign, relationship, remote
from sqlalchemy_utils import LtreeType

from models.base import Base


class TextEntityBase(Base):
    __abstract__ = True

    text = Column(Text, nullable=False)


class Post(TextEntityBase):
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    author = relationship("User", primaryjoin="Post.author_id == User.id")


class Comment(TextEntityBase):
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("post.id"), nullable=False)
    node_path = Column(LtreeType, nullable=False)
    parent = relationship(
        "Comment",
        primaryjoin=(remote(node_path) == foreign(func.subpath(node_path, 0, -1))),
        backref="children",
        viewonly=True,
    )

    __table_args__ = (Index("ix_nodes_path", node_path, postgresql_using="gist"),)


class PostUpvote(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey("post.id"), nullable=False, index=True)
    positive = Column(Boolean, default=True)


class CommentUpvote(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True)
    comment_uuid = Column(UUID(as_uuid=True), ForeignKey("comment.id"), nullable=False, index=True)
    positive = Column(Boolean, default=True)
