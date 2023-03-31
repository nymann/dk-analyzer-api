import requests

from dk_analyzer_api.domain.warcraft_logs.auth.service import WarcraftLogsAuthService


class WarcraftLogsApi:
    def __init__(
        self,
        warcraft_logs_auth_service: WarcraftLogsAuthService,
    ) -> None:
        self._warcraft_logs_auth_service = warcraft_logs_auth_service

    def _headers(self) -> dict[str, str]:
        access_token = self._warcraft_logs_auth_service.get_access_token().access_token
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

    def _fetch(self, body: str) -> requests.Response:
        response = requests.post(
            "https://www.warcraftlogs.com/api/v2/client",
            headers=self._headers(),
            json={"query": body},
            timeout=5,
        )
        response.raise_for_status()
        return response
