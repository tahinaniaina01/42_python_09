#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   space_crew.py                                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: trakotos <trakototrakotos@student.42antana   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/18 11:01:14 by trakotos            #+#    #+#            #
#   Updated: 2026/04/18 14:59:41 by trakotos           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from datetime import datetime
from typing import Any, List
from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import Enum

class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank = Field(...)
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)

    @classmethod
    def create_crew_member(cls, crew_data: dict[str, Any]) -> "CrewMember":
        crew = cls(
            member_id = crew_data["member_id"],
            name = crew_data["name"],
            rank = crew_data["rank"],
            age = crew_data["age"],
            specialization = crew_data["specialization"],
            years_experience = crew_data["years_experience"],
            is_active = crew_data["is_active"]
        )
        return crew
    
    def show(self) -> None:
        print(f"{self.name} ({self.rank}) - {self.specialization}")


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime = Field(...)
    duration_days: int = Field(..., ge=1, le=3650)
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_space_mission(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("mission ID must start with 'M'")
        has_senior_officer = any(
            m.rank in (Rank.COMMANDER, Rank.CAPTAIN)
            for m in self.crew
        )
        if not has_senior_officer:
            raise ValueError("Mission must have at least one Commander or Captain")
        if self.duration_days > 365:
            experienced_crew = sum(1 for m in self.crew if m.years_experience >= 5)
            if experienced_crew / len(self.crew) < 0.5:
                raise ValueError("Long missions (> 365 days) need 50%% experienced crew (5+ years)")
        inactive_member = [member for member in self.crew if not member.is_active]
        if inactive_member:
            raise ValueError("All crew members must be active")
        return self
    
    @classmethod
    def create_space_mission(cls, space_mission_data: dict[str, Any]) -> "SpaceMission":
        space_mission = cls(
            mission_id = space_mission_data["mission_id"],
            mission_name = space_mission_data["mission_name"],
            destination = space_mission_data["destination"],
            launch_date = space_mission_data["launch_date"],
            duration_days = space_mission_data["duration_days"],
            crew = [CrewMember.create_crew_member(data) for data in space_mission_data["crew"]],
            mission_status = space_mission_data["mission_status"],
            budget_millions = space_mission_data["budget_millions"],
        )
        return space_mission
    
    def show(self) -> None:
        print(f"Mission: {self.mission_name}")
        print(f"ID: {self.mission_id}")
        print(f"Destination: {self.destination}")
        print(f"Duration: {self.duration_days} days")
        print(f"Budget: ${self.budget_millions}M")
        print(f"Crew size: {len(self.crew)}")
        print(f"Crew members:")
        for crew_member in self.crew:
            print(end="- ")
            crew_member.show()
        print()

def main() -> None:
    space_mission_datas = [
        {
            "mission_id": "M2024_MARS",
            "mission_name": "Mars Colony Establishment",
            "destination": "Mars",
            "launch_date": datetime(2026, 7, 1, 9, 0, 0),
            "duration_days": 900,
            "crew": [
                {
                    "member_id": "S001",
                    "name": "Sarah Connor",
                    "rank": "commander",
                    "age": 35,
                    "specialization": "Mission Command",
                    "years_experience": 10,
                    "is_active": True
                },
                {
                    "member_id": "J002",
                    "name": "John Smith",
                    "rank": "lieutenant",
                    "age": 40,
                    "specialization": "Navigation",
                    "years_experience": 6,
                    "is_active": True
                },
                {
                    "member_id": "A003",
                    "name": "Alice Johnson",
                    "rank": "officer",
                    "age": 30,
                    "specialization": "Engineering",
                    "years_experience": 2,
                    "is_active": True
                }
            ],
            "mission_status": "planned",
            "budget_millions": 2500.0
        }
    ]
    print("Space Mission Crew Validation")
    for data in space_mission_datas:
        try:
            print("=" * 40)
            s = SpaceMission.create_space_mission(data)
            print("Valid mission created:")
            s.show()
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