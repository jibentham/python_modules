from pydantic import BaseModel, Field, ValidationError, model_validator
from datetime import datetime
from typing import Union
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
    signal_strength: float = Field(ge=0.0, le=10.0, decimal_places=1)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Union[str, None] = Field(max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_model(self) -> Self:
        if not (self.contact_id.startswith("AC")):
            raise ValueError("Contact ID must start with 'AC' (Alien Contact)")
        if (self.contact_type == ContactType.physical and not self.is_verified):
            raise ValueError("Physical contact reports must be verified")
        if (self.contact_type == ContactType.telepathic and self.witness_count < 3):
            raise ValueError("Telepathic contact requires at least 3 witnesses")
        if (self.signal_strength > 7.0 and not self.message_received):
            raise ValueError("Strong signals (> 7.0) should include received messages")
        return self

