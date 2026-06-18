from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from typing import Union
from enum import Enum


class Rank(Enum):
    cadet = 1
    officer = 2
    lieutenant = 3
    captain = 4
    commander = 5


class CrewMemberModel(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMissionModel(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMemberModel] = Field(min_items=1, max_items=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0, decimal_places=2)

    @model_validator(mode='after')
    def validate_model(self) -> Self:
        if not (self.mission_id.startswith("M")):
            raise ValueError("Mission ID must start with 'M'")
        if not (any(member.rank in (Rank.commander, Rank.captain) for member in self.crew)):
            raise ValueError("Must have at least one Commander or Captain")
        experienced: int = sum(1 for member in self.crew if member.years_experience >= 5)
        if self.duration_days > 365 and (experienced / len(self.crew)) < 0.5:
            raise ValueError("Long missions (> 365 days) need 50% experienced crew (5+ years)")
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self
