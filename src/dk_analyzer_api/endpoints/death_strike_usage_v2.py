from dk_analyzer.models import Event
from dk_analyzer.warcraftlogs import fetch_report
from dk_analyzer.warcraftlogs import get_access_token
from pogo_api.endpoint import GetEndpoint
from pydantic import BaseModel


class DeathStrike(BaseModel):
    x: float  # noqa: WPS111
    y: float  # noqa: WPS111
    r: float = 2  # noqa: WPS111


class DeathStrikes(BaseModel):
    mean_hp: float
    mean_rp: float
    data: list[DeathStrike]  # noqa: WPS110


class Mean(BaseModel):
    rp: float
    hp: float

    @classmethod
    def from_events(cls, events: list[Event]) -> "Mean":
        hp = 0
        rp = 0
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


class DeathStrikeUsageBubbleChart(GetEndpoint):
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = get_access_token(
            client_id=client_id,
            client_secret=client_secret,
        )
        super().__init__()

    async def endpoint(self, report_id: str, fight_id: int = 1) -> DeathStrikes:
        events = fetch_report(
            report_id=report_id,
            fight_id=fight_id,
            access_token=self.access_token,
        )
        return self._convert_events(events=events)

    def _transform_events(self, events: list[Event]) -> dict[float, dict[float, DeathStrike]]:
        temp_data: dict[float, dict[float, DeathStrike]] = {}
        for event in events:
            if not event.is_cast_by_player():
                continue
            hp = event.hp_percent()
            rp = event.rp()
            if rp not in temp_data:
                temp_data[rp] = {}
            if hp in temp_data[rp]:
                temp_data[rp][hp].r += 1  # noqa: WPS529
                continue
            temp_data[rp][hp] = DeathStrike(x=rp, y=hp)
        return temp_data

    def _convert_events(self, events: list[Event]) -> DeathStrikes:
        temp_data: dict[float, dict[float, DeathStrike]] = self._transform_events(events=events)
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
