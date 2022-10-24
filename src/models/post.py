from sqlalchemy import Boolean, Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base import Base

"""
Comment threading logic at DB level:

1) When creating comment without parent_comment_id, new thread being populated (thread-0),
comment with parent_comment_id inherits parent's thread_id.

[Post]
  |
  | [thread-0  primary=True]  (primary means thread attached directly to the post, not comment)
  L__ [comment-0]
      L__ [comment-1]
          L__ [comment-2]


2) When creating comment with parent_comment_id that already exists in DB, new thread is
being populated with primary=False.

[Post]
  |
  | [thread-0 primary=True]
  L__ [comment-0]
  |   L__ [comment-1]
  |       L__ [comment-2]
  |       |
  |       | [thread-1 primary=False]
  |       L__ [comment-3]
  |       |   L__ [comment-4]
  |       |
  |       | [thread-2 primary=False]
  |       L__ [comment-3]
  |
  | [thread-3 primary=True]
  L__ [comment-5]

Attaching comments to each other being managed only by threads logic.



Comment threading logic at API level:

1) GET /thread/?post_id=XXXX
returns primary threads attached to post_id

2) GET /comment/?thread_id=YYYY&offset=0&limit=10
returns list of comments in the thread, with following structure:

{
id: UUID4,
attached_thread: UUID4 | None,
threads_attached_to_comment: list[UUID4],
...
}

"""


class TextEntityBase(Base):
    __abstract__ = True

    text = Column(Text, nullable=False)


class Post(TextEntityBase):
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    author = relationship("User", primaryjoin="Post.author_id == User.id")


class Comment(TextEntityBase):
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    attached_to_thread_id = Column(UUID(as_uuid=True), ForeignKey("commentthread.id"), nullable=False, index=True)
    # attached_to_thread = relationship("CommentThread", foreign_keys=[attached_to_thread_id])
    attached_threads = relationship("CommentThread", foreign_keys="[CommentThread.comment_id]", uselist=True)


class CommentThread(Base):
    post_id = Column(UUID(as_uuid=True), ForeignKey("post.id"), nullable=True, index=True)
    comment_id = Column(UUID(as_uuid=True), ForeignKey("comment.id"), nullable=True, index=True)
    # comment = relationship("Comment", back_populates="attached_threads", foreign_keys=[comment_id])


class PostUpvote(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey("post.id"), nullable=False, index=True)
    positive = Column(Boolean, default=True)


class CommentUpvote(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True)
    comment_uuid = Column(UUID(as_uuid=True), ForeignKey("comment.id"), nullable=False, index=True)
    positive = Column(Boolean, default=True)
