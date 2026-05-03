# FreeMedia: Simple infrastructure for hosting different kinds of media.
#     Copyright (C) 2026  Anatnaso
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SAEnum
from sqlmodel import Field, SQLModel

from .post_status import PostStatus


class MediaPost(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str = Field(default="[PLACEHOLDER]", min_length=3, max_length=50)
    description: str = Field(default="")

    status: PostStatus = Field(
        default=PostStatus.DRAFT,
        sa_column=Column(SAEnum(PostStatus)),
    )

    primary_file_id: int | None = Field(default=None, foreign_key="mediafile.id")

    datetime_created: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.now(timezone.utc),
    )
