from dk_analyzer.models import Event
from dk_analyzer.warcraftlogs import fetch_report
from dk_analyzer.warcraftlogs import get_access_token
from pogo_api.endpoint import GetEndpoint
from pydantic import BaseModel

class DeathStrikes(BaseModel):
    hp_list: list[float]
    rp_list: list[float]

class DeathStrikeUsage(GetEndpoint):
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = get_access_token(
            client_id=client_id,
            client_secret=client_secret,
        )
        super().__init__()

    async def endpoint(self, report_id: str, fight_id: int) -> DeathStrikes:
        events = fetch_report(
            report_id=report_id,
            fight_id=fight_id,
            access_token=self.access_token,
        )
        return self._convert_events(events=events)

    def _convert_events(self, events: list[Event]) -> DeathStrikes:
        hp_list: list[float] = []
        rp_list: list[float] = []
        for event in events:
            if not event.is_cast_by_player():
                continue
            hp_list.append(event.hp_percent())
            rp_list.append(event.rp())
        return DeathStrikes(hp_list=hp_list, rp_list=rp_list)
