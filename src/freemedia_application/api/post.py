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

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from freemedia_database import get_session
from freemedia_database.media_post import MediaPost

router = APIRouter(prefix="/post", tags=["post"])


@router.post("/")
async def post_post(post: MediaPost, session: Session = Depends(get_session)):
    session.add(post)
    session.commit()
    session.refresh(post)

    return post


@router.get("/")
async def get_posts(session: Session = Depends(get_session)):
    stmt = select(MediaPost)
    posts = session.exec(stmt).all()

    return posts


@router.get("/{post_id}")
async def get_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(MediaPost, post_id)

    return post
