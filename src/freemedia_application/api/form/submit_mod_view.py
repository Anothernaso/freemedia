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

from fastapi import APIRouter, Form, Query, status
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/submit_mod_view", tags=["submit_mod_view"])


@router.post("/")
async def post_submit_mod_view(
    admin_token: str = Query(...),
    post_id: int = Form(...),
):
    return RedirectResponse(
        f"/page/view_post/{post_id}?admin_token={admin_token}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
