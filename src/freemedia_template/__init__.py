# FreeMedia: Simple infrastructure for hosting different kinds of media.
#     Copyright (C) 2026  Anatnaso
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


from typing import Any

from fastapi.templating import Jinja2Templates

from freemedia_miscellaneous.notice import get_notice_text
from freemedia_settings import get_settings

_templates: Jinja2Templates | None = None
_context: dict[str, str] | None = None


def get_templates() -> Jinja2Templates:
    global _templates

    if not _templates:
        _templates = Jinja2Templates(directory="template")

    return _templates


def get_context(additional_context: dict[Any, Any] = {}) -> dict[str, str]:
    global _context

    settings = get_settings()

    if not _context:
        _context = {
            "freemedia_application_title": settings.freemedia_application_title,
            "freemedia_legal_notice": get_notice_text(),
        }

    return _context | additional_context
