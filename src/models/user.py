from sqlmodel import Field
from sqlmodel.sql.expression import Select, SelectOfScalar

from models.base import ModelBase

SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore


class User(ModelBase, table=True):
    username: str = Field(nullable=False, index=True, sa_column_kwargs={"unique": True})
    password: str
