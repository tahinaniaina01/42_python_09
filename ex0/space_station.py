#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   space_station.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: trakotos <trakototrakotos@student.42antana   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/18 08:54:41 by trakotos            #+#    #+#            #
#   Updated: 2026/04/18 15:01:53 by trakotos           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Any
from datetime import datetime

class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime = Field(...)
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)

    def show(self) -> None:
        print(f"ID: {self.station_id}")
        print(f"Name: {self.name}")
        print(f"Crew: {self.crew_size} people")
        print(f"Power: {self.power_level}%")
        print(f"Oxygen: {self.oxygen_level}%")
        print(f"Status: {'Operational' if self.is_operational else 'Offline'}\n")

    @classmethod
    def create_station(cls, station_data: dict[str, Any]) -> "SpaceStation":
        station = cls(
            station_id=station_data["station_id"],
            name=station_data["name"],
            crew_size=station_data["crew_size"],
            power_level=station_data["power_level"],
            oxygen_level=station_data["oxygen_level"],
            is_operational=station_data["is_operational"],
            last_maintenance=station_data["last_maintenance"]
        )
        return station

def main() -> None:
    print("Space Station Data Validation")
    stations_datas = [
        {
            "station_id": "ISS001",
            "name": "International Space Station",
            "crew_size": 6,
            "power_level": 85.5,
            "oxygen_level": 92.3,
            "is_operational": True,
            "last_maintenance": "2024-01-15T10:30:00"
        },
        {
            "station_id": "ISS001",
            "name": "International Space Station",
            "crew_size": 67,
            "power_level": 185.5,
            "oxygen_level": 92.3,
            "is_operational": True,
            "last_maintenance": "2024-01-15T10:30:00"
        }
    ]
    for station_data in stations_datas:
        try:
            print("=" * 40)
            station = SpaceStation.create_station(station_data)
            print("Valid station created:")
            station.show()
        except ValidationError as error:
            print("Expected validation error:")
            for err in error.errors():
                print(err["msg"])
        except Exception as error:
            print(f"[ERROR] {error}")

if __name__ == "__main__":
    main()