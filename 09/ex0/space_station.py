from pydantic import BaseModel, Field
from datetime import datetime
from typing import Union
from pydantic import ValidationError


class SpaceStationModel(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Union[str, None] = Field(max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("================================================")
    print("Valid station created:")
    try:
        valid_station: SpaceStationModel = SpaceStationModel(
                station_id="ISS001",
                name="International Space Station",
                crew_size=6,
                power_level=85.5,
                oxygen_level=92.3,
                last_maintenance="2026-06-27T14:30:00",
                is_operational=True,
                notes=None
                )
        print(f"ID: {valid_station.station_id}")
        print(f"Name: {valid_station.name}")
        print(f"Crew: {valid_station.crew_size} people")
        print(f"Power: {valid_station.power_level}%")
        print(f"Oxygen: {valid_station.oxygen_level}%")
        print(
            f"""Status:
             {'Operational' if valid_station.is_operational
              else 'Not operational'}"""
            )
        print("\n================================================")
    except ValidationError as e:
        print(f"Validation failed: {e.errors()[0]['msg']}")
    print("Expected validation error:")
    try:
        SpaceStationModel(
                station_id="ISS001",
                name="International Space Station",
                crew_size=55,
                power_level=85.5,
                oxygen_level=92.3,
                last_maintenance="2026-06-27T14:30:00",
                is_operational=True,
                notes=None
                )
    except ValidationError as e:
        print(f"Validation failed: {e.errors()[0]['msg']}")


if __name__ == "__main__":
    main()
