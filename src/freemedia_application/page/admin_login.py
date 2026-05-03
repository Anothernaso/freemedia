from fastapi import APIRouter, Request

from freemedia_template import get_context, get_templates

router = APIRouter(prefix="/admin_login", tags=["admin_login"])


@router.get("/{session_expired}")
async def get_admin_login(request: Request, session_expired: bool):
    templates = get_templates()

    return templates.TemplateResponse(
        request,
        name="page/admin_login.html",
        context=await get_context(
            {"freemedia_request_session_expired": session_expired}
        ),
    )
