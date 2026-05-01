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

from pydantic_settings import BaseSettings, SettingsConfigDict


class FreeMediaSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    freemedia_uvicorn_host: str = "localhost"
    freemedia_uvicorn_port: int = 4678
    freemedia_uvicorn_workers: int = 4
    freemedia_uvicorn_reload: bool = False

    freemedia_database_url: str = "postgresql://default:secret@localhost:5432/freemedia"
    freemedia_database_echo: bool = False

    freemedia_application_title: str = "FreeMedia"


settings = FreeMediaSettings()
