import logging

from dk_analyzer_api.domain.warcraft_logs.death_strikes.models.healing import ClassResource
from dk_analyzer_api.domain.warcraft_logs.death_strikes.models.healing import Datum


class Event:
    def __init__(self, event: Datum) -> None:
        self._event = event
        self.current_hp = event.hit_points
        self.heal_amount = event.amount
        self.hp_before = self.current_hp - self.heal_amount
        self.max_hp = event.max_hit_points
        self._rp: ClassResource = event.class_resources[0]

    def hp_percent(self) -> float:
        if self.hp_before - self.max_hp > 0:
            logging.error("Higher than 100%% HP?? %s", self._event)  # noqa: WPS323
            return 100.0
        return (self.hp_before / self.max_hp) * 100

    def rp(self) -> float:
        return self._rp.amount / 10

    def is_cast_by_player(self) -> bool:
        return self._rp.max != 0
