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


from asyncio import to_thread

from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from freemedia_settings import get_settings

from .administration_session import AdministrationSession
from .media_file import MediaFile
from .media_post import MediaPost
from .post_status import PostStatus

__all__ = ["AdministrationSession", "MediaFile", "MediaPost", "PostStatus"]


_engine: Engine | None = None


async def get_engine() -> Engine:
    global _engine

    settings = await get_settings()

    if not _engine:
        _engine = await to_thread(
            create_engine,
            settings.freemedia_database_url,
            echo=settings.freemedia_database_echo,
        )

    return _engine


async def create_metadata() -> None:
    await to_thread(SQLModel.metadata.create_all, await get_engine())


async def get_session() -> Session:
    return await to_thread(Session, await get_engine())
