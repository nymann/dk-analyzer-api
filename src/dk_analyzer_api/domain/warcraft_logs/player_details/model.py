from pydantic import Field

from dk_analyzer_api.core.base import Base


class Spec(Base):
    spec: str
    count: int


class Player(Base):
    name: str
    id: int
    guid: int
    type: str
    server: str
    icon: str
    specs: list[Spec]
    min_item_level: int = Field(..., alias="minItemLevel")
    max_item_level: int = Field(..., alias="maxItemLevel")
    potion_use: int = Field(..., alias="potionUse")
    healthstone_use: int = Field(..., alias="healthstoneUse")
    combatant_info: list = Field(..., alias="combatantInfo")


class PlayerDetailsData(Base):
    dps: list[Player]
    healers: list[Player]
    tanks: list[Player]


class PlayerDetailsDataWrapper(Base):
    player_details: PlayerDetailsData = Field(..., alias="playerDetails")


class PlayerDetails(Base):
    data: PlayerDetailsDataWrapper = Field(..., alias="data")


class Report(Base):
    player_details: PlayerDetails = Field(..., alias="playerDetails")


class ReportData(Base):
    report: Report


class Data(Base):
    report_data: ReportData = Field(..., alias="reportData")


class Model(Base):
    data: Data
