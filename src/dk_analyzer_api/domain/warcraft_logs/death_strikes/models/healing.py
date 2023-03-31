from typing import Any, Optional

from pydantic import Field

from dk_analyzer_api.core.base import Base


class ClassResource(Base):
    amount: int
    max: int
    type: int


class Datum(Base):
    timestamp: int
    type: str
    source_id: int = Field(..., alias="sourceID")
    target_id: int = Field(..., alias="targetID")
    ability_game_id: int = Field(..., alias="abilityGameID")
    fight: int
    buffs: str
    hit_type: int = Field(..., alias="hitType")
    amount: int
    overheal: Optional[int] = None
    resource_actor: int = Field(..., alias="resourceActor")
    class_resources: list[ClassResource] = Field(..., alias="classResources")
    hit_points: int = Field(..., alias="hitPoints")
    max_hit_points: int = Field(..., alias="maxHitPoints")
    attack_power: int = Field(..., alias="attackPower")
    spell_power: int = Field(..., alias="spellPower")
    armor: int
    absorb: int
    x: int
    y: int
    facing: int
    map_id: int = Field(..., alias="mapID")
    item_level: int = Field(..., alias="itemLevel")
    source_marker: Optional[int] = Field(None, alias="sourceMarker")
    target_marker: Optional[int] = Field(None, alias="targetMarker")
    source_instance: Optional[int] = Field(None, alias="sourceInstance")
    target_instance: Optional[int] = Field(None, alias="targetInstance")
    absorbed: Optional[int] = None


class Events(Base):
    data: list[Datum]
    next_page_timestamp: Any = Field(..., alias="nextPageTimestamp")


class Report(Base):
    events: Events


class ReportData(Base):
    report: Report


class Data(Base):
    report_data: ReportData = Field(..., alias="reportData")


class Model(Base):
    data: Data
