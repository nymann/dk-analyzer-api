from fastapi import FastAPI
from pogo_api.endpoint import Endpoint

from dk_analyzer_api.core.config import Config
from dk_analyzer_api.core.service_container import ServiceContainer
from dk_analyzer_api.endpoints.death_strike_usage import DeathStrikeUsage


class Api:
    def __init__(self, config: Config, service_container: ServiceContainer) -> None:
        self.api = FastAPI(version=config.version, title=config.title, docs_url="/")
        self.config = config
        self.services = service_container
        self.add_endpoints()

    @property
    def endpoints(self) -> list[Endpoint]:
        return [
            DeathStrikeUsage(
                client_id=self.config.warcraftlogs_client_id,
                client_secret=self.config.warcraftlogs_client_secret,
            ),
        ]

    def add_endpoints(self) -> None:
        for endpoint in self.endpoints:
            endpoint.route.add_to_router(self.api)
