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

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from freemedia_application.utility.admin_auth import try_admin_login
from freemedia_database import get_session
from freemedia_template import get_context, get_templates

router = APIRouter(prefix="/admin_panel", tags=["admin_panel"])


@router.get("/")
async def get_admin_panel(
    request: Request, admin_token: str, session: Session = Depends(get_session)
):
    templates = get_templates()

    result = await try_admin_login(admin_token, session)
    if result:
        return result

    return templates.TemplateResponse(
        request,
        name="page/admin_panel.html",
        context=await get_context({}),
    )
