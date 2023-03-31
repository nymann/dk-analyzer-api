from dk_analyzer_api.core.exceptions import NotFound
from dk_analyzer_api.domain.warcraft_logs.api import WarcraftLogsApi
from dk_analyzer_api.domain.warcraft_logs.player_details.model import Model
from dk_analyzer_api.domain.warcraft_logs.player_details.model import Player
from dk_analyzer_api.domain.warcraft_logs.player_details.model import PlayerDetailsData


class WarcraftLogsPlayerDetailsService(WarcraftLogsApi):
    def get_blood_dk(self, report_id: str, fight_id: int) -> Player:
        players = self._get_player_details(report_id=report_id, fight_id=fight_id)
        tanks = players.tanks
        for tank in tanks:
            if tank.icon == "DeathKnight-Blood":
                return tank
        raise NotFound(detail=f"No Blood Death Knight found in report_id={report_id}, fight_id={fight_id}")

    def _get_player_details(self, report_id: str, fight_id: int) -> PlayerDetailsData:
        body = f"""
query {{
    reportData {{
        report(code:"{report_id}"){{
            playerDetails(fightIDs:{fight_id})
        }}
    }}
}}
        """
        response = self._fetch(body=body)
        return Model(**response.json()).data.report_data.report.player_details.data.player_details  # noqa: WPS219
