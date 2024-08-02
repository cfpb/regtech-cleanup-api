import os
from urllib import parse
from typing import Any

from pydantic import field_validator, ValidationInfo
from pydantic.networks import PostgresDsn
from pydantic_settings import BaseSettings

from regtech_api_commons.oauth2.config import KeycloakSettings
from regtech_regex.regex_config import RegexConfigs

env_files_to_load = [".env"]
if os.getenv("ENV", "LOCAL") == "LOCAL":
    file_dir = os.path.dirname(os.path.realpath(__file__))
    env_files_to_load.append(f"{file_dir}/../.env.local")


class Settings(BaseSettings):
    db_schema: str = "public"
    db_name: str
    db_user: str
    db_pwd: str
    db_host: str
    db_scheme: str = "postgresql+asyncpg"
    db_logging: bool = False
    conn: PostgresDsn | None = None

    def __init__(self, **data):
        super().__init__(**data)

    @field_validator("conn", mode="before")
    @classmethod
    def build_postgres_dsn(cls, postgres_dsn, info: ValidationInfo) -> Any:
        postgres_dsn = PostgresDsn.build(
            scheme=info.data.get("db_scheme"),
            username=info.data.get("db_user"),
            password=parse.quote(info.data.get("db_pwd"), safe=""),
            host=info.data.get("db_host"),
            path=info.data.get("db_name"),
        )
        return str(postgres_dsn)


settings = Settings()

kc_settings = KeycloakSettings(_env_file=env_files_to_load)

regex_configs = RegexConfigs.instance()
