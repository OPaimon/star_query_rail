import secrets

from pydantic import BaseSettings


class Setting(BaseSettings):
    dbname: str = "starrail"
    url: str = f"postgresql://postgres:@localhost/{dbname}"
    echo: bool = True
    SECRET_KEY: str = secrets.token_urlsafe(32)


settings = Setting()
