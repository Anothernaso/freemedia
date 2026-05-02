from fastapi import APIRouter, Request

from freemedia_template import get_context, get_templates

router = APIRouter(prefix="/home", tags=["home"])


@router.get("/")
async def get_home(request: Request):
    templates = get_templates()

    return templates.TemplateResponse(
        request, name="page/home.html", context=get_context()
    )
