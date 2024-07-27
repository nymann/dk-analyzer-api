from dk_analyzer_api.core.exceptions import NotFound
from dk_analyzer_api.domain.warcraft_logs.api import WarcraftLogsApi
from dk_analyzer_api.domain.warcraft_logs.report_fights.model import Report


class WarcraftLogsReportFightsService(WarcraftLogsApi):
    def get_report(self, url: str) -> Report:
        try:
            report = Report.from_url(url)
        except Exception:
            raise NotFound(f"Report or fight not found ('{url}')")
        if report.fight_id is None:
            return self._get_last_report(report.report_id)
        return report

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
