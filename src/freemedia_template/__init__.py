from fastapi.templating import Jinja2Templates

from freemedia_miscellaneous import notice
from freemedia_settings import settings

templates = Jinja2Templates(directory="template")
context: dict[str, str] = {
    "freemedia_application_title": settings.freemedia_application_title,
    "freemedia_legal_notice": notice.notice_text,
}
