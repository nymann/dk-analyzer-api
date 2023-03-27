from pydantic import BaseSettings

from dk_analyzer_api.version import __version__


class Config(BaseSettings):
    title: str
    version: str = __version__

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
