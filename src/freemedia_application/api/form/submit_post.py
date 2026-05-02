from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlmodel import Session

from freemedia_database import get_session
from freemedia_database.media_post import MediaPost

router = APIRouter(prefix="/submit_post", tags=["submit_post"])


@router.post("/")
async def post_submit_post(
    title: str | None = Form(None),
    description: str | None = Form(None),
    session: Session = Depends(get_session),
):
    post = MediaPost()
    if title:
        post.title = title
    if description:
        post.description = description

    session.add(post)
    session.commit()
    session.refresh(post)

    return RedirectResponse(f"/page/view_post/{post.id}", status_code=303)
