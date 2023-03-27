from dk_analyzer_api.api import Api
from dk_analyzer_api.core.config import Config
from dk_analyzer_api.core.service_container import ServiceContainer

config = Config()  # type: ignore
service_container = ServiceContainer(config=config)
api = Api(config=config, service_container=service_container).api
