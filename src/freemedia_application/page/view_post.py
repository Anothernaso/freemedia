from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session

from freemedia_database import MediaPost, get_session
from freemedia_template import get_context, get_templates

router = APIRouter(prefix="/view_post", tags=["view_post"])


@router.get("/{post_id}")
async def get_view_post(
    request: Request, post_id: int, session: Session = Depends(get_session)
):
    templates = get_templates()

    post = session.get(MediaPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail=f"No such post: {post_id}")

    return templates.TemplateResponse(
        request=request,
        name="page/view_post.html",
        context=get_context(
            {
                "freemedia_request_post_id": post.id,
                "freemedia_request_post_title": post.title,
                "freemedia_request_post_description": post.description,
            }
        ),
    )
