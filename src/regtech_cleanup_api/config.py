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


class Institution_Settings(BaseSettings):
    user_fi_db_schema: str = "public"
    user_fi__db_name: str
    user_fi_db_user: str
    user_fi_db_pwd: str
    user_fi_db_host: str
    user_fi_db_scheme: str = "postgresql+asyncpg"
    user_fi_db_logging: bool = False
    conn: PostgresDsn | None = None

    def __init__(self, **data):
        super().__init__(**data)

    @field_validator("conn", mode="before")
    @classmethod
    def build_postgres_dsn(cls, postgres_dsn, info: ValidationInfo) -> Any:
        postgres_dsn = PostgresDsn.build(
            scheme=info.data.get("user_fi_db_scheme"),
            username=info.data.get("user_fi_db_user"),
            password=parse.quote(info.data.get("use_fi_db_pwd"), safe=""),
            host=info.data.get("user_fi_db_host"),
            path=info.data.get("user_fi_db_name"),
        )
        return str(postgres_dsn)


class Filing_Settings(BaseSettings):
    filing_db_schema: str = "public"
    filing_db_name: str
    filing_db_user: str
    filing_db_pwd: str
    filing_db_host: str
    filing_db_scheme: str = "postgresql+asyncpg"
    filing_db_logging: bool = False
    conn: PostgresDsn | None = None

    def __init__(self, **data):
        super().__init__(**data)

    @field_validator("conn", mode="before")
    @classmethod
    def build_postgres_dsn(cls, postgres_dsn, info: ValidationInfo) -> Any:
        postgres_dsn = PostgresDsn.build(
            scheme=info.data.get("filing_db_scheme"),
            username=info.data.get("filing_db_user"),
            password=parse.quote(info.data.get("filing_db_pwd"), safe=""),
            host=info.data.get("filing_db_host"),
            path=info.data.get("filing_db_name"),
        )
        return str(postgres_dsn)


user_fi_settings = Institution_Settings()
filing_settings = Filing_Settings()


kc_settings = KeycloakSettings(_env_file=env_files_to_load)

regex_configs = RegexConfigs.instance()
