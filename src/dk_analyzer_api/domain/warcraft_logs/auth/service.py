import requests

from dk_analyzer_api.core.config import WarcraftLogsConfig
from dk_analyzer_api.domain.warcraft_logs.auth.model import Token


class WarcraftLogsAuthService:
    def __init__(self, config: WarcraftLogsConfig) -> None:
        self._client_id = config.client_id
        self._client_secret = config.client_secret
        self._token: Token = self._get_access_token()

    def get_access_token(self) -> Token:
        if not self._token.is_expired():
            return self._token
        return self._get_access_token()

    def _get_access_token(self) -> Token:
        response = requests.post(
            "https://www.warcraftlogs.com/oauth/token",
            data={"grant_type": "client_credentials"},
            auth=(self._client_id, self._client_secret),
            timeout=5,
        )
        self._token = Token.from_api(**response.json())
        return self._token
