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

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session

from freemedia_database import MediaPost, PostStatus, get_session
from freemedia_template import get_context, get_templates

router = APIRouter(prefix="/view_post", tags=["view_post"])


@router.get("/{post_id}")
async def get_view_post(
    request: Request, post_id: int, session: Session = Depends(get_session)
):
    templates = get_templates()

    post = await to_thread(session.get, MediaPost, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No such post: {post_id}"
        )

    if post.status != PostStatus.PUBLISHED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Post has not been published: {post_id}",
        )

    return templates.TemplateResponse(
        request,
        name="page/view_post.html",
        context=await get_context(
            {
                "freemedia_request_post_id": post.id,
                "freemedia_request_post_title": post.title,
                "freemedia_request_post_description": post.description,
            }
        ),
    )
