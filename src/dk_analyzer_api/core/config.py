from pydantic import BaseSettings

from dk_analyzer_api.version import __version__


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class WarcraftLogsConfig(BaseConfig):
    client_id: str
    client_secret: str

    class Config:
        env_prefix = "warcraft_logs_"


class AppConfig(BaseConfig):
    title: str


class Config:
    def __init__(self) -> None:
        self.version = __version__
        self.warcraft_logs = WarcraftLogsConfig()  # type:ignore
        self.app = AppConfig()  # type: ignore
