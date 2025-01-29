import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pogo_api.endpoint import Endpoint

from dk_analyzer_api.core.config import Config
from dk_analyzer_api.core.service_container import ServiceContainer
from dk_analyzer_api.endpoints.death_strike_usage import DeathStrikeUsageBubbleChart


class Api:
    def __init__(self, config: Config, service_container: ServiceContainer) -> None:
        logging.basicConfig(level="INFO", format="%(levelname)s:\t%(asctime)s\t%(message)s")  # noqa: WPS323
        self.api = FastAPI(version=config.version, title=config.app.title, docs_url="/")
        self.config = config
        self.services = service_container
        self._add_endpoints()
        self._add_middleware()

    @property
    def endpoints(self) -> list[Endpoint]:
        return [DeathStrikeUsageBubbleChart(death_strike_service=self.services.death_strike_service())]

    def _add_middleware(self) -> None:
        self.api.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _add_endpoints(self) -> None:
        for endpoint in self.endpoints:
            endpoint.route.add_to_router(self.api)
