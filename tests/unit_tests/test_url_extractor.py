from dataclasses import dataclass

import pytest

from dk_analyzer_api.domain.url_extractor import ReportFight
from dk_analyzer_api.domain.warcraft_logs.auth.service import WarcraftLogsAuthService
from dk_analyzer_api.domain.warcraft_logs.report_fights.service import WarcraftLogsReportFightsService


@dataclass
class TestCase:
    url: str
    expected_report_id: str
    expected_fight_id: str


test_cases: list[TestCase] = [
    TestCase(
        url="https://www.warcraftlogs.com/reports/MyvF2p1m7Df4VLjH/#fight=25",
        expected_report_id="MyvF2p1m7Df4VLjH",
        expected_fight_id="25",
    ),
    TestCase(
        url="https://fr.warcraftlogs.com/reports/Rhzw1yxZHCFTQNd2#fight=last",
        expected_report_id="Rhzw1yxZHCFTQNd2",
        expected_fight_id="last",
    ),
    TestCase(
        url="https://www.warcraftlogs.com/reports/MyvF2p1m7Df4VLjH#fight=25",
        expected_report_id="MyvF2p1m7Df4VLjH",
        expected_fight_id="25",
    ),
]


@pytest.mark.parametrize("test_case", test_cases)
def test_bla(test_case: TestCase):
    actual = ReportFight.from_url(test_case.url)
    assert test_case.expected_report_id == actual.report_id
    assert test_case.expected_fight_id == actual.fight_id
