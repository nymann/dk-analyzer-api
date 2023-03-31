from pydantic import BaseModel

from dk_analyzer_api.domain.death_strike.model import Event
from dk_analyzer_api.domain.warcraft_logs.death_strikes.service import WarcraftLogsDeathStrikeService
from dk_analyzer_api.domain.warcraft_logs.report_fights.service import WarcraftLogsReportFightsService


class DeathStrike(BaseModel):
    x: float  # noqa: WPS111
    y: float  # noqa: WPS111
    r: float = 0  # noqa: WPS111
    count: int = 0

    def add(self, base_bubble_size: float) -> None:
        self.count += 1  # noqa: WPS601
        self.r += base_bubble_size  # noqa: WPS601 WPS111


class DeathStrikes(BaseModel):
    mean_hp: float
    mean_rp: float
    data: list[DeathStrike]  # noqa: WPS110


class Mean(BaseModel):
    rp: float
    hp: float

    @classmethod
    def from_events(cls, events: list[Event]) -> "Mean":
        hp: float = 0
        rp: float = 0
        count = 0
        for event in events:
            if not event.is_cast_by_player():
                continue
            hp += event.hp_percent()
            rp += event.rp()
            count += 1
        if count == 0:
            return cls(rp=0, hp=0)
        return cls(rp=rp / count, hp=hp / count)


class DeathStrikeService:
    def __init__(
        self,
        warcraft_logs_death_strike_service: WarcraftLogsDeathStrikeService,
        warcraft_logs_report_fights: WarcraftLogsReportFightsService,
    ) -> None:
        self._warcraft_logs_death_strike_service = warcraft_logs_death_strike_service
        self._warcraft_logs_report_fights_service = warcraft_logs_report_fights

    def get_events(self, url: str, base_bubble_size: float) -> DeathStrikes:
        report = self._warcraft_logs_report_fights_service.get_report(url=url)
        events = self._warcraft_logs_death_strike_service.get_healing_events(report=report)
        converted = [Event(event) for event in events]
        return self._convert_events(converted, base_bubble_size)

    def _transform_events(
        self,
        events: list[Event],
        base_bubble_size: float,
    ) -> dict[float, dict[float, DeathStrike]]:
        temp_data: dict[float, dict[float, DeathStrike]] = {}
        for event in events:
            if not event.is_cast_by_player():
                continue
            hp = event.hp_percent()
            rp = event.rp()
            if rp not in temp_data:
                temp_data[rp] = {}
            if hp not in temp_data[rp]:
                temp_data[rp][hp] = DeathStrike(x=rp, y=hp)
            temp_data[rp][hp].add(base_bubble_size=base_bubble_size)
        return temp_data

    def _convert_events(self, events: list[Event], base_bubble_size: float) -> DeathStrikes:
        temp_data: dict[float, dict[float, DeathStrike]] = self._transform_events(
            events=events,
            base_bubble_size=base_bubble_size,
        )
        death_strikes: list[DeathStrike] = []
        for hp_dict in temp_data.values():
            for death_strike in hp_dict.values():
                death_strikes.append(death_strike)

        mean = Mean.from_events(events=events)
        return DeathStrikes(
            mean_hp=mean.hp,
            mean_rp=mean.rp,
            data=death_strikes,
        )
