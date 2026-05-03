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
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi import Path as FPath
from fastapi.responses import FileResponse
from sqlmodel import Session

from freemedia_application.utility.admin_auth import try_admin_login
from freemedia_database import MediaFile, MediaPost, PostStatus, get_session
from freemedia_settings import get_settings

router = APIRouter(prefix="/file", tags=["file"])


@router.get("/{file_id}")
async def get_file(
    file_id: int = FPath(...),
    admin_token: str | None = Query(default=None),
    session: Session = Depends(get_session),
):

    settings = await get_settings()

    file = await to_thread(session.get, MediaFile, file_id)
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No such file: {file_id}"
        )

    filepath = Path(settings.freemedia_mediafile_directory) / str(file.id)

    if not filepath.exists():
        raise Exception(
            f"Could not find filesystem file `{filepath}` referenced by zombie file `{file.id}`"
        )

    post = await to_thread(session.get, MediaPost, file.post_id)
    if not post:
        raise Exception(
            f"Could not find post `{file.post_id}` referenced by zombie file `{file.id}`"
        )

    #######################
    ## STATE CHECK BEGIN ##
    #######################

    is_admin: bool = False
    if admin_token:
        result = await try_admin_login(admin_token, session)
        if result:
            return result
        else:
            is_admin = True

    if post.status == PostStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Post has not been submitted: {post.id}",
        )

    if not is_admin and post.status == PostStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Post has not been published: {post.id}",
        )

    #######################
    ## FILE STREAM BEGIN ##
    #######################

    return FileResponse(
        path=filepath,
        filename=file.filename,
        # TODO: Use actual mimetype of file
        media_type="application/octet-stream",
    )
