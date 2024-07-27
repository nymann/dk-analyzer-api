from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from dk_analyzer_api.version import __version__


class WarcraftLogsConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="warcraft_logs_",
        extra="allow",
    )
    client_id: str
    client_secret: str


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    title: str


class Config:
    def __init__(self) -> None:
        self.version = __version__
        self.warcraft_logs = WarcraftLogsConfig()  # type: ignore
        self.app = AppConfig()  # type: ignore
