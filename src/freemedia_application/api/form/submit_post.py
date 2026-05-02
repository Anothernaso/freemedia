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
