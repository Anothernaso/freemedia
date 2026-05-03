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

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from freemedia_database import (
    AdministrationSession,
    IncidentReport,
    IncidentType,
    get_session,
)
from freemedia_settings import get_settings

router = APIRouter(prefix="/submit_admin_login", tags=["submit_admin_login"])


@router.post("/")
async def post_submit_post(
    request: Request,
    passphrase: str = Form(...),
    session: Session = Depends(get_session),
):
    settings = await get_settings()

    if passphrase != settings.freemedia_administration_passphrase:
        report = IncidentReport(
            type=IncidentType.UNAUTHORIZED_ADMINISTRATOR,
            endpoint=request.url.path,
            client_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        await to_thread(session.add, report)
        await to_thread(session.commit)
        await to_thread(session.refresh, report)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Wrong administration passphrase: {passphrase}; this incident will be reported.",
        )

    admin_session = AdministrationSession()
    await to_thread(session.add, admin_session)
    await to_thread(session.commit)
    await to_thread(session.refresh, admin_session)

    return RedirectResponse(
        f"/page/admin_panel?admin_token={admin_session.token}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
