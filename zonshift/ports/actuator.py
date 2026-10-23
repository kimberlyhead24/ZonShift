""" Copyright (C) 2026 Kimberly Head 
SPDX-License-Identifier: GPL-3.0-or-later."""
from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class ActuatorState:
    zone_id: str
    is_active: bool
    intensity_perc: float

class ActuatorPort(Protocol):
    def set_state(self, zone_id: str, active: bool, intensity: float) -> ActuatorState:
        """Command the physical hardware or simulation to change state."""
        ...
