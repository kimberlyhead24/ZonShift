""" Copyright (C) 2026 Kimberly Head 
SPDX-License-Identifier: GPL-3.0-or-later."""
"""Simulated sensor adapter: reads values from in-memory Zones."""
from __future__ import annotations

from datetime import datetime, timezone

from zonshift.errors import UnknownZoneError
from zonshift.ports.sensor import Quality, Reading
from zonshift.simulation import Zone


class SimulatedSensor:
    """Satisfies SensorPort by reporting the simulator's current values."""

    def __init__(self, zones: dict[str, Zone]) -> None:
        self._zones = zones

    def read(self, zone_id: str) -> Reading:
        """Return the latest reading. Time O(V), space O(V).

        Raises:
            UnknownZoneError: If ``zone_id`` is not registered.
        """
        try:
            zone = self._zones[zone_id]
        except KeyError as exc:
            raise UnknownZoneError(f"unknown zone {zone_id!r}") from exc
        return Reading(
            zone_id=zone_id,
            values={n: v.current for n, v in zone.variables.items()},
            observed_at=datetime.now(timezone.utc),
            quality=Quality.SIMULATED,
        )
