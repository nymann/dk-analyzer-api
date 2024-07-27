import logging

from dk_analyzer_api.core.exceptions import NotFound
from dk_analyzer_api.domain.warcraft_logs.api import WarcraftLogsApi
from dk_analyzer_api.domain.warcraft_logs.report_fights.model import Report


class WarcraftLogsReportFightsService(WarcraftLogsApi):
    def get_report(self, url: str) -> Report:
        try:
            fight_id = self._get_fight_id(url)
            report_id = self._get_report_id(url)
        except Exception:
            raise NotFound(f"Report or fight not found ('{url}')")
        if fight_id == "last":
            return self._get_last_report(report_id=report_id)
        return Report(report_id=report_id, fight_id=fight_id)

    def _get_report_id(self, url: str) -> str:
        # https://www.warcraftlogs.com/reports/MyvF2p1m7Df4VLjH/#fight=25
        # https://www.warcraftlogs.com/reports/MyvF2p1m7Df4VLjH#fight=25
        s = url.split("reports/")[1]
        b = s.split("#fight=")[0]
        logging.info(b)
        return b.replace("/", "")

    def _get_fight_id(self, url: str) -> int:
        # https://www.warcraftlogs.com/reports/MyvF2p1m7Df4VLjH/#fight=25
        # https://www.warcraftlogs.com/reports/MyvF2p1m7Df4VLjH#fight=25
        s = url.split("#fight=")[1]
        logging.info(s)
        return int(s)

    def _get_last_report(self, report_id: str) -> Report:
        body = f"""
query {{
    reportData {{
        report(code:"{report_id}"){{
            fights {{
                id
            }}
        }}
    }}
}}
        """
        response = self._fetch(body=body)
        fights = response.json()["data"]["reportData"]["report"]["fights"]
        fight_id = int(fights[-1]["id"])
        return Report(report_id=report_id, fight_id=fight_id)
