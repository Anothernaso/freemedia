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
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, Response, status
from sqlmodel import Session, select
from starlette.responses import RedirectResponse

from freemedia_database import AdministrationSession
from freemedia_settings import get_settings


async def try_admin_login(admin_token: str, session: Session) -> Response | None:
    settings = await get_settings()

    statement = await to_thread(
        (await to_thread(select, AdministrationSession)).where,
        AdministrationSession.token == admin_token,
    )
    admin_session = await to_thread(
        (await to_thread(session.exec, statement)).first,
    )

    if admin_session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid administration session token: {admin_token}",
        )

    delta = datetime.now(timezone.utc) - admin_session.datetime_created

    if delta > timedelta(
        minutes=settings.freemedia_administration_session_lifetime_minutes
    ):
        await to_thread(session.delete, admin_session)
        await to_thread(session.commit)

        return RedirectResponse(
            "/page/admin_login?session_expired=True",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return None
