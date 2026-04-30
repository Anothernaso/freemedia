from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .media_file import MediaFile


class MediaPost(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str = Field(min_length=3, max_length=50)
    description: str

    primary_file_id: int | None = Field(default=None, foreign_key="media_file.id")
    primary_file: MediaFile | None = Relationship()

    files: list[MediaFile] = Relationship(back_populates="post")
