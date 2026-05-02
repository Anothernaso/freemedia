from fastapi import APIRouter, Request

from freemedia_template import get_context, get_templates

router = APIRouter(prefix="/create_post", tags=["create_post"])


@router.get("/")
async def get_create_post(request: Request):
    templates = get_templates()

    return templates.TemplateResponse(
        request=request,
        name="page/create_post.html",
        context=get_context(),
    )
