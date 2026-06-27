from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from typing import Self
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
    crew: list[CrewMemberModel] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_model(self) -> Self:
        if not (self.mission_id.startswith("M")):
            raise ValueError("Mission ID must start with 'M'")
        if not (
            any(member.rank in (
                Rank.commander, Rank.captain
            ) for member in self.crew)
        ):
            raise ValueError("Must have at least one Commander or Captain")
        experienced: int = (
            sum(1 for member in self.crew if member.years_experience >= 5)
        )
        if self.duration_days > 365 and (experienced / len(self.crew)) < 0.5:
            raise ValueError(
                """Long missions (> 365 days)
                 need 50 percent experienced crew (5+ years)"""
                )
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("================================================")
    try:
        valid_mission = SpaceMissionModel(
            mission_id="M0001",
            mission_name="Mars Expedition Alpha",
            destination="Mars",
            launch_date=datetime(2026, 9, 1, 8, 0, 0),
            duration_days=300,
            crew=[
                CrewMemberModel(
                    member_id="CM001",
                    name="Jane Foster",
                    rank=Rank.commander,
                    age=45,
                    specialization="Navigation",
                    years_experience=20,
                    is_active=True,
                ),
                CrewMemberModel(
                    member_id="CM002",
                    name="John Smith",
                    rank=Rank.officer,
                    age=35,
                    specialization="Engineering",
                    years_experience=10,
                    is_active=True,
                ),
                CrewMemberModel(
                    member_id="CM003",
                    name="Sara Lee",
                    rank=Rank.lieutenant,
                    age=30,
                    specialization="Medicine",
                    years_experience=7,
                    is_active=True,
                ),
            ],
            mission_status="planned",
            budget_millions=500.0,
        )
        print(f"Mission ID: {valid_mission.mission_id}")
        print(f"Mission Name: {valid_mission.mission_name}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Launch Date: {valid_mission.launch_date}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Crew Size: {len(valid_mission.crew)}")
        print(f"Status: {valid_mission.mission_status}")
        print("Crew members:")
        for member in valid_mission.crew:
            print(
                f"""  - {member.name}
                 ({member.rank.name})
                  - {member.specialization}"""
                )
        print(f"Budget: ${valid_mission.budget_millions}M")
        print("\n================================================")
    except ValidationError as e:
        print(f"Validation failed: {e.errors()[0]['msg']}")
    print("Expected validation error:")
    try:
        SpaceMissionModel(
            mission_id="M0001",
            mission_name="Mars Expedition Beta",
            destination="Mars",
            launch_date=datetime(2026, 9, 1, 8, 0, 0),
            duration_days=100,
            crew=[
                CrewMemberModel(
                    member_id="CM001",
                    name="Jane Foster",
                    rank=Rank.officer,
                    age=45,
                    specialization="Navigation",
                    years_experience=20,
                    is_active=True,
                ),
                CrewMemberModel(
                    member_id="CM002",
                    name="John Smith",
                    rank=Rank.officer,
                    age=35,
                    specialization="Engineering",
                    years_experience=10,
                    is_active=True,
                ),
                CrewMemberModel(
                    member_id="CM003",
                    name="Sara Lee",
                    rank=Rank.lieutenant,
                    age=30,
                    specialization="Medicine",
                    years_experience=7,
                    is_active=True,
                ),
            ],
            budget_millions=100.0,
        )
    except ValidationError as e:
        print(f"Validation failed: {e.errors()[0]['msg']}")


if __name__ == "__main__":
    main()
