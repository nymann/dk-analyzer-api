from dataclasses import dataclass


@dataclass
class ReportFight:
    report_id: str
    fight_id: str

    @classmethod
    def from_url(cls, url: str) -> "ReportFight":
        report_id = url.split("reports/")[1].split("#fight=")[0].replace("/", "")
        fight_id = url.split("#fight=")[1]
        return cls(report_id=report_id, fight_id=fight_id)
