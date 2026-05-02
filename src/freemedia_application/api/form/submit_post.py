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

from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from freemedia_database import get_session
from freemedia_database.media_post import MediaPost
from freemedia_database.post_status import PostStatus

router = APIRouter(prefix="/submit_post", tags=["submit_post"])


@router.post("/")
async def post_submit_post(
    title: str | None = Form(None),
    description: str | None = Form(None),
    session: Session = Depends(get_session),
):
    post = MediaPost()
    post.status = PostStatus.PENDING
    if title:
        post.title = title
    if description:
        post.description = description

    session.add(post)
    session.commit()
    session.refresh(post)

    return RedirectResponse(
        f"/page/submission_notice/{post.id}", status_code=status.HTTP_303_SEE_OTHER
    )
