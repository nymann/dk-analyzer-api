from typing import Optional

from pydantic import BaseModel


class Report(BaseModel):
    report_id: str
    fight_id: Optional[int] = None

    @classmethod
    def from_url(cls, url: str) -> "Report":
        fight_id = url.split("reports/")[1]
        b = fight_id.split("#fight=")[0]
        report_id = b.replace("/", "")
        fight_id = url.split("#fight=")[1]
        if fight_id == "last":
            return Report(report_id=report_id)
        return Report(report_id=report_id, fight_id=int(fight_id))
