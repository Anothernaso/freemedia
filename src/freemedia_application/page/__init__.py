from fastapi import APIRouter, Request

from freemedia_template import context, templates

router = APIRouter(prefix="/page", tags=["page"])


@router.get("/home")
async def get_home(request: Request):
    return templates.TemplateResponse(
        request=request, name="home.html", context=context
    )
