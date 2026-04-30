from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .media_file import MediaFile


class MediaPost(SQLModel, table=True):
    id: int | None = Field(default=None, nullable=False, unique=True, primary_key=True)

    title: str = Field(nullable=False, min_length=3, max_length=50)
    description: str = Field(nullable=False)

    primary_file: int | None = Field(
        default=None, nullable=True, foreign_key="media_file.id"
    )

    files: list[MediaFile] = Relationship(back_populates="post")
