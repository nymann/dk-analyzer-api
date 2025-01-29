import logging

from dk_analyzer_api.core.exceptions import NotFound
from dk_analyzer_api.domain.url_extractor import ReportFight
from dk_analyzer_api.domain.warcraft_logs.api import WarcraftLogsApi
from dk_analyzer_api.domain.warcraft_logs.report_fights.model import Report


class WarcraftLogsReportFightsService(WarcraftLogsApi):
    def get_report(self, url: str) -> Report:
        try:
            report_fight = ReportFight.from_url(url)
            if report_fight.fight_id == "last":
                return self._get_last_report(report_fight.report_id)
            return Report(report_id=report_fight.report_id, fight_id=int(report_fight.fight_id))
        except Exception as e:
            logging.error(e)
            raise NotFound(f"Report or fight not found ('{url}')")

    def _get_last_report(self, report_id: str) -> Report:
        body = f"""
query {{
    reportData {{
        report(code:"{report_id}"){{
            fights {{
                id
                friendlyPlayers
            }}
        }}
    }}
}}
        """
        response = self._fetch(body=body)
        fights = response.json()["data"]["reportData"]["report"]["fights"]
        for fight in reversed(fights):
            friendly_players = fight["friendlyPlayers"]
            if len(friendly_players) < 5:
                continue
            fight_id = int(fight["id"])
            return Report(report_id=report_id, fight_id=fight_id)
        raise NotFound(f"Couldn't find valid fight for report '{report_id}'")
