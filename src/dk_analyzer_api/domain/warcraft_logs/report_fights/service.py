from dk_analyzer_api.core.exceptions import NotFound
from dk_analyzer_api.domain.warcraft_logs.api import WarcraftLogsApi
from dk_analyzer_api.domain.warcraft_logs.report_fights.model import Report


class WarcraftLogsReportFightsService(WarcraftLogsApi):
    def get_report(self, url: str) -> Report:
        report_id, fight_id = self._extract_report_id_and_fight_id(url=url)
        if fight_id == "last":
            return self._get_last_report(report_id=report_id)
        try:
            fight_id_int = int(fight_id)
        except Exception:
            raise NotFound("Report or fight not found")
        return Report(report_id=report_id, fight_id=fight_id_int)

    def _extract_report_id_and_fight_id(self, url: str) -> tuple[str, str | int]:
        try:
            report_id, fight_id = url.split("reports/")[1].split("/#fight=")
        except Exception:
            raise NotFound("Report or fight not found")
        return report_id, fight_id

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
