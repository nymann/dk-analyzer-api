from dk_analyzer_api.domain.warcraft_logs.api import WarcraftLogsApi
from dk_analyzer_api.domain.warcraft_logs.auth.service import WarcraftLogsAuthService
from dk_analyzer_api.domain.warcraft_logs.death_strikes.models.healing import Datum
from dk_analyzer_api.domain.warcraft_logs.death_strikes.models.healing import Model
from dk_analyzer_api.domain.warcraft_logs.player_details.service import WarcraftLogsPlayerDetailsService
from dk_analyzer_api.domain.warcraft_logs.report_fights.model import Report


class WarcraftLogsDeathStrikeService(WarcraftLogsApi):
    def __init__(
        self,
        warcraft_logs_auth_service: WarcraftLogsAuthService,
        player_details_service: WarcraftLogsPlayerDetailsService,
    ) -> None:
        self._player_details_service = player_details_service
        super().__init__(warcraft_logs_auth_service=warcraft_logs_auth_service)

    def get_healing_events(self, report: Report) -> list[Datum]:
        bdk = self._player_details_service.get_blood_dk(report=report)
        body = f"""
query {{
    reportData {{
        report(code:"{report.report_id}"){{
            events(
                fightIDs:{report.fight_id},
                abilityID:45470,
                sourceID:{bdk.id},
                dataType:Healing,
                includeResources:true,
                limit:9000
            ) {{
                data
                nextPageTimestamp
            }}
        }}
    }}
}}
        """
        response = self._fetch(body=body)
        return Model(**response.json()).data.report_data.report.events.data  # noqa: WPS219
