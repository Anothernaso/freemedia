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

import shutil
from asyncio import to_thread
from pathlib import Path
from typing import cast

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from freemedia_database import get_session
from freemedia_database.media_file import MediaFile
from freemedia_database.media_post import MediaPost
from freemedia_database.post_status import PostStatus
from freemedia_settings import get_settings

router = APIRouter(prefix="/submit_post", tags=["submit_post"])


@router.post("/")
async def post_submit_post(
    title: str | None = Form(None),
    description: str | None = Form(None),
    files: list[UploadFile] = File(...),
    session: Session = Depends(get_session),
):
    settings = await get_settings()

    post = MediaPost()
    post.status = PostStatus.DRAFT
    if title:
        post.title = title
    if description:
        post.description = description

    await to_thread(session.add, post)
    await to_thread(session.commit)
    await to_thread(session.refresh, post)

    media_file_dir = Path(settings.freemedia_media_file_directory)
    await to_thread(media_file_dir.mkdir, parents=True, exist_ok=True)

    for index, file in enumerate(files):
        filename: str
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File must have filename: {index}",
            )

        filename = file.filename

        media_file = MediaFile(
            filename=filename,
            post_id=cast(int, post.id),
        )

        await to_thread(session.add, media_file)
        await to_thread(session.commit)
        await to_thread(session.refresh, media_file)

        def write_file() -> None:
            with open(media_file_dir / str(media_file.id), "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        await to_thread(write_file)

    # Only set the post to `PENDING` after all properties have been set
    post.status = PostStatus.PENDING

    await to_thread(session.commit)
    await to_thread(session.refresh, post)

    return RedirectResponse(
        f"/page/submission_notice/{post.id}", status_code=status.HTTP_303_SEE_OTHER
    )
