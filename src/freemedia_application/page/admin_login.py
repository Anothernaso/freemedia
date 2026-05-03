from fastapi import APIRouter, Request

from freemedia_template import get_context, get_templates

router = APIRouter(prefix="/admin_login", tags=["admin_login"])


@router.get("/")
async def get_admin_login(request: Request):
    templates = get_templates()

    return templates.TemplateResponse(
        request, name="page/admin_login.html", context=await get_context()
    )
