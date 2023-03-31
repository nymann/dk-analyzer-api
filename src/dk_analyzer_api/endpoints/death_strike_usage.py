from pogo_api.endpoint import GetEndpoint

from dk_analyzer_api.domain.death_strike.service import DeathStrikeService
from dk_analyzer_api.domain.death_strike.service import DeathStrikes


class DeathStrikeUsageBubbleChart(GetEndpoint):
    def __init__(self, death_strike_service: DeathStrikeService) -> None:
        self._death_strike_service = death_strike_service
        super().__init__()

    async def endpoint(
        self,
        report_id: str,
        fight_id: int = 1,
        base_bubble_size: float = 2.0,
    ) -> DeathStrikes:
        return self._death_strike_service.get_events(
            report_id=report_id,
            fight_id=fight_id,
            base_bubble_size=base_bubble_size,
        )
