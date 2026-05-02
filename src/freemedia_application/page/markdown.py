from fastapi import APIRouter, Request

from freemedia_template import get_context, get_templates

router = APIRouter(prefix="/markdown", tags=["markdown"])


@router.get("/{static_path:path}")
async def get_markdown(request: Request, static_path: str):
    templates = get_templates()

    return templates.TemplateResponse(
        request,
        name="page/markdown.html",
        context=get_context(
            {
                "freemedia_request_static_path": "/" + static_path,
            }
        ),
    )
