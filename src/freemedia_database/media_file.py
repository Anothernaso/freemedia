from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .media_post import MediaPost


class MediaFile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    post_id: int = Field(foreign_key="media_post.id")
    post: MediaPost = Relationship(back_populates="files")
