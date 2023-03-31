from dk_analyzer_api.core.config import Config
from dk_analyzer_api.domain.death_strike.service import DeathStrikeService
from dk_analyzer_api.domain.warcraft_logs.auth.service import WarcraftLogsAuthService
from dk_analyzer_api.domain.warcraft_logs.death_strikes.service import WarcraftLogsDeathStrikeService
from dk_analyzer_api.domain.warcraft_logs.player_details.service import WarcraftLogsPlayerDetailsService
from dk_analyzer_api.domain.warcraft_logs.report_fights.service import WarcraftLogsReportFightsService


class ServiceContainer:
    def __init__(self, config: Config) -> None:
        self.config = config

    def death_strike_service(self) -> DeathStrikeService:
        return DeathStrikeService(
            warcraft_logs_death_strike_service=WarcraftLogsDeathStrikeService(
                warcraft_logs_auth_service=self.auth_service(),
                player_details_service=self.player_details_service(),
            ),
            warcraft_logs_report_fights=self.report_fights_service(),
        )

    def report_fights_service(self) -> WarcraftLogsReportFightsService:
        return WarcraftLogsReportFightsService(warcraft_logs_auth_service=self.auth_service())

    def auth_service(self) -> WarcraftLogsAuthService:
        return WarcraftLogsAuthService(config=self.config.warcraft_logs)

    def player_details_service(self) -> WarcraftLogsPlayerDetailsService:
        return WarcraftLogsPlayerDetailsService(warcraft_logs_auth_service=self.auth_service())
