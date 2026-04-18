#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   alien_contact.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: trakotos <trakototrakotos@student.42antana   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/18 10:05:01 by trakotos            #+#    #+#            #
#   Updated: 2026/04/18 14:08:19 by trakotos           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from typing import Any, Optional

class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"

class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime = Field(...)
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType = Field(...)
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    is_verified: bool = Field(default=False)
    message_received: Optional[str] = Field(default=None, max_length=500)

    @model_validator(mode='after')
    def validate_cantact_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contanct ID must start with AC")
        
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        
        if self.contact_type == ContactType.TELEPATHIC and self.witness_count < 3:
            raise ValueError("Telepathic contact requires at least 3 witness")

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) should include a received message")
        
        return self
    
    @classmethod
    def create_alien_contact(cls, station_data: dict[str, Any]) -> "AlienContact":
        station = cls(
            contact_id=station_data["contact_id"],
            timestamp=station_data["timestamp"],
            location=station_data["location"],
            contact_type=station_data["contact_type"],
            signal_strength=station_data["signal_strength"],
            duration_minutes=station_data["duration_minutes"],
            witness_count=station_data["witness_count"],
            message_received=station_data["message_received"]
        )
        return station

    def show(self) -> None:
        print(f"ID: {self.contact_id}")
        print(f"Type: {self.contact_type}")
        print(f"Location: {self.location}")
        print(f"Signal: {self.signal_strength}/10")
        print(f"Duration: {self.duration_minutes} minutes")
        print(f"Witnesses: {self.witness_count}")
        print(f"Message: '{self.message_received}'")
        print()
    
def main() -> None:
    stations_datas = [
        {
            "contact_id": "AC_2024_001",
            "timestamp": "2024-01-15T10:30:00",
            "location": "Area 51, Nevada",
            "contact_type": "radio",
            "signal_strength": 8.5,
            "duration_minutes": 45,
            "witness_count": 5,
            "message_received": "Greetings from Zeta Reticuli"
        },
        {
            "contact_id": "AC_2024_001",
            "timestamp": "2024-01-15T10:30:00",
            "location": "Area 51, Nevada",
            "contact_type": "telepathic",
            "signal_strength": 8.5,
            "duration_minutes": 45,
            "witness_count": 2,
            "message_received": "Greetings from Zeta Reticuli"
        },
    ]
    
    for station_data in stations_datas:
        try:
            print("=" * 40)
            station = AlienContact.create_alien_contact(station_data)
            print("Valid station created:")
            station.show()
        except ValidationError as error:
            print("Expected validation error:")
            for err in error.errors():
                if "Value error" in err["msg"]:
                    err["msg"] = err["msg"][13:]
                print(err["msg"])
        except Exception as error:
            print(f"[ERROR] {error}")

if __name__ == "__main__":
    main()