from datetime import datetime, timezone
from secrets import token_urlsafe

from sqlmodel import Field, SQLModel


class AdministrationSession(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    token: str = Field(default_factory=lambda: token_urlsafe(), unique=True)

    datetime_created: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
