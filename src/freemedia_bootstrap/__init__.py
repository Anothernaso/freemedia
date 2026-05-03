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

import asyncio

import uvicorn

from freemedia_miscellaneous.notice import get_notice_text
from freemedia_settings import get_settings


def main() -> None:
    settings = asyncio.run(get_settings())

    print(get_notice_text() + "\n")

    uvicorn.run(
        "freemedia_application:app",
        host=settings.freemedia_uvicorn_host,
        port=settings.freemedia_uvicorn_port,
        workers=settings.freemedia_uvicorn_workers,
        reload=settings.freemedia_uvicorn_reload,
    )


if __name__ == "__main__":
    main()
