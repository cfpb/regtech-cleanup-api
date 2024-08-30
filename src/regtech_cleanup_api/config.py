import os

from regtech_api_commons.oauth2.config import KeycloakSettings
from regtech_regex.regex_config import RegexConfigs

from sbl_filing_api.config import Settings as Filing_Settings
from regtech_user_fi_management.config import Settings as Institution_Settings
from pathlib import Path


env_files_to_load: list[Path | str] = [".env"]
if os.getenv("ENV", "LOCAL") == "LOCAL":
    env_files_to_load.append(".env.local")

institution_settings = Institution_Settings()
filing_settings = Filing_Settings()
kc_settings = KeycloakSettings(_env_file=env_files_to_load)
regex_configs = RegexConfigs.instance()
