from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session

from freemedia_database import MediaPost, PostStatus, get_session
from freemedia_template import get_context, get_templates

router = APIRouter(prefix="/submission_notice", tags=["submission_notice"])


@router.get("/{post_id}")
async def get_submission_notice(
    request: Request, post_id: int, session: Session = Depends(get_session)
):

    post = session.get(MediaPost, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No such post: {post_id}"
        )

    if post.status != PostStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Post is not pending review: {post_id}",
        )

    templates = get_templates()

    return templates.TemplateResponse(
        request,
        "page/submission_notice.html",
        context=get_context(
            {
                "freemedia_request_post_id": post_id,
            }
        ),
    )
