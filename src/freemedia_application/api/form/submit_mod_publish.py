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

from fastapi import APIRouter, Depends, Form, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from freemedia_application.utility.admin_auth import try_admin_login
from freemedia_database import (
    MediaPost,
    PostStatus,
    get_session,
)

router = APIRouter(prefix="/submit_mod_publish", tags=["submit_mod_publish"])


@router.post("/")
async def post_submit_mod_publish(
    admin_token: str = Query(...),
    view_post: bool = Form(default=False),
    post_id: int = Form(...),
    session: Session = Depends(get_session),
):
    result = await try_admin_login(admin_token, session)
    if result:
        return result

    post = await to_thread(session.get, MediaPost, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No such post: {post_id}"
        )

    if post.status == PostStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Post has not been submitted: {post_id}",
        )

    if post.status == PostStatus.PUBLISHED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Post is already published: {post_id}",
        )

    post.status = PostStatus.PUBLISHED
    await to_thread(session.commit)
    await to_thread(session.refresh, post)

    return (
        RedirectResponse(
            f"/page/view_post/{post_id}",
            status_code=status.HTTP_303_SEE_OTHER,
        )
        if view_post
        else RedirectResponse(
            f"/page/admin_panel?admin_token={admin_token}",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    )
