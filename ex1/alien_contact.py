#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   alien_contact.py                                     :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: trakotos <trakototrakotos@student.42antana   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/18 10:05:01 by trakotos            #+#    #+#            #
#   Updated: 2026/04/18 10:33:17 by trakotos           ###   ########.fr      #
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
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

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