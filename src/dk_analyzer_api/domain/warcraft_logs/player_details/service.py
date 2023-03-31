from dk_analyzer_api.core.exceptions import NotFound
from dk_analyzer_api.domain.warcraft_logs.api import WarcraftLogsApi
from dk_analyzer_api.domain.warcraft_logs.player_details.model import Model
from dk_analyzer_api.domain.warcraft_logs.player_details.model import Player
from dk_analyzer_api.domain.warcraft_logs.player_details.model import PlayerDetailsData
from dk_analyzer_api.domain.warcraft_logs.report_fights.model import Report


class WarcraftLogsPlayerDetailsService(WarcraftLogsApi):
    def get_blood_dk(self, report: Report) -> Player:
        players = self._get_player_details(report_id=report.report_id, fight_id=report.fight_id)
        tanks = players.tanks
        for tank in tanks:
            if tank.icon == "DeathKnight-Blood":
                return tank
        raise NotFound(detail="No Blood Death Knight found for that report")

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
