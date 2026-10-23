""" Copyright (C) 2026 Kimberly Head 
SPDX-License-Identifier: GPL-3.0-or-later."""

"""Sensor port: the interface the core uses to read zone conditions.

Any object with a matching ``read`` method satisfies ``SensorPort``;
it does not need to inherit from it (structural typing, PEP 544).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Protocol


class Quality(Enum):
    """How trustworthy a reading is."""

    GOOD = "good"            # measured by a calibrated sensor
    ESTIMATED = "estimated"  # derived, such as runtime-based energy
    SIMULATED = "simulated"  # produced by the simulator
    BAD = "bad"              # sensor fault or out-of-range value


@dataclass(frozen=True)
class Reading:
    """An immutable snapshot of one zone's conditions.

    Attributes:
        zone_id: Zone the reading belongs to.
        values: Variable name to value, such as {"temperature": 87.0}.
        observed_at: When the value was measured (timezone-aware UTC).
        quality: How much to trust the values.
    """

    zone_id: str
    values: dict[str, float]
    observed_at: datetime
    quality: Quality


class SensorPort(Protocol):
    """Anything that can report the latest reading for a zone."""

    def read(self, zone_id: str) -> Reading:
        """Return the latest reading for a zone.

        Args:
            zone_id: Identifier of the zone, such as "tropical".

        Returns:
            The most recent Reading for that zone.

        Raises:
            UnknownZoneError: If no zone has that identifier.
        """
        ...
