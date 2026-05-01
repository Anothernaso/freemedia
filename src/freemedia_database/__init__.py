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


from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from freemedia_settings import settings

from .media_file import MediaFile
from .media_post import MediaPost

__all__ = ["MediaFile", "MediaPost"]


_engine: Engine | None = None


def get_engine() -> Engine:
    global _engine

    if not _engine:
        _engine = create_engine(settings.freemedia_database_url, echo=True)

    return _engine


def create_metadata() -> None:
    SQLModel.metadata.create_all(get_engine())


def get_session() -> Session:
    return Session(get_engine())
