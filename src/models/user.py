from sqlmodel import Field, Relationship
from sqlmodel.sql.expression import Select, SelectOfScalar

from models.base import ModelBase

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


class User(ModelBase, table=True):
    username: str = Field(nullable=False, index=True, sa_column_kwargs={"unique": True})
    password: str

    sessions: list["Session"] = Relationship(back_populates="user")
    posts: list["Post"] = Relationship(back_populates="author")
    comments: list["Comment"] = Relationship(back_populates="author")
    post_upvotes: list["PostUpvote"] = Relationship(back_populates="user")
    comment_upvotes: list["CommentUpvote"] = Relationship(back_populates="user")
