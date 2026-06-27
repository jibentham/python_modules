from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from typing import Union, Self
from enum import Enum


class ContactType(Enum):
    radio = 1
    visual = 2
    physical = 3
    telepathic = 4


class AlienContactModel(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Union[str, None] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_model(self) -> Self:
        if not (self.contact_id.startswith("AC")):
            raise ValueError("Contact ID must start with 'AC' (Alien Contact)")
        if (
            self.contact_type == ContactType.physical and not self.is_verified
        ):
            raise ValueError("Physical contact reports must be verified")
        if (
            self.contact_type == ContactType.telepathic
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
                )
        if (self.signal_strength > 7.0 and not self.message_received):
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
                )
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("================================================")
    try:
        valid_contact = AlienContactModel(
            contact_id="AC001",
            timestamp=datetime(2026, 6, 27, 14, 30, 0),
            location="Roswell, New Mexico",
            contact_type=ContactType.radio,
            signal_strength=5.5,
            duration_minutes=30,
            witness_count=3,
            message_received="Beep boop",
            is_verified=True,
        )
        print(f"Contact ID: {valid_contact.contact_id}")
        print(f"Timestamp: {valid_contact.timestamp}")
        print(f"Location: {valid_contact.location}")
        print(f"Type: {valid_contact.contact_type.name}")
        print(f"Signal Strength: {valid_contact.signal_strength}")
        print(f"Duration: {valid_contact.duration_minutes} minutes")
        print(f"Witnesses: {valid_contact.witness_count}")
        print(f"Message: {valid_contact.message_received}")
        print(f"Verified: {valid_contact.is_verified}")
        print("\n================================================")
    except ValidationError as e:
        print(f"Validation failed: {e.errors()[0]['msg']}")
    print("Expected validation error:")
    try:
        AlienContactModel(
            contact_id="AC001",
            timestamp=datetime(2026, 6, 27, 14, 30, 0),
            location="Roswell, New Mexico",
            contact_type=ContactType.telepathic,
            signal_strength=5.5,
            duration_minutes=30,
            witness_count=1,
            is_verified=True,
        )
    except ValidationError as e:
        print(f"Validation failed: {e.errors()[0]['msg']}")


if __name__ == "__main__":
    main()
