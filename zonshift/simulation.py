""" Copyright (C) 2026 Kimberly Head
SPDX-License-Identifier: GPL-3.0-or-later."""

"""Generic climate simulation for user-defined grow zones.

A Zone owns named Variables (temperature, humidity, light, CO2, ...) and
Devices that push those variables up or down. Nothing here is hardcoded to
particular crops or equipment, so any zone shape can be described as data.
Pure logic with no I/O.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from zonshift.errors import InvalidValueError


def _require_finite(label: str, value: float) -> None:
    """Raise InvalidValueError if value is NaN or infinite. O(1)."""
    if not math.isfinite(value):
        raise InvalidValueError(f"{label} must be a finite number, got {value!r}")


@dataclass
class Variable:
    """A controlled quantity inside a zone.

    Attributes:
        name: Key such as "temperature". Must match its key in Zone.variables.
        unit: Display unit, such as "F", "%", or "umol/m2/s".
        current: Present value.
        target: Desired value.
        minimum: Lowest physically allowed value.
        maximum: Highest physically allowed value.

    Raises:
        InvalidValueError: If a value is not finite, minimum exceeds
            maximum, or current/target fall outside the allowed range.
    """

    name: str
    unit: str
    current: float
    target: float
    minimum: float = -math.inf
    maximum: float = math.inf

    def __post_init__(self) -> None:
        _require_finite(f"{self.name}.current", self.current)
        _require_finite(f"{self.name}.target", self.target)
        if math.isnan(self.minimum) or math.isnan(self.maximum):
            raise InvalidValueError(f"{self.name} limits cannot be NaN")
        if self.minimum > self.maximum:
            raise InvalidValueError(f"{self.name}: minimum exceeds maximum")
        for label, value in (("current", self.current), ("target", self.target)):
            if not self.minimum <= value <= self.maximum:
                raise InvalidValueError(
                    f"{self.name}.{label}={value} is outside "
                    f"[{self.minimum}, {self.maximum}]"
                )


@dataclass
class Device:
    """Equipment that pushes one variable up and/or down.

    Attributes:
        name: Unique name within its zone.
        metric: Name of the Variable it affects.
        raise_rate_per_hour: Units per hour it can add (0 if it cannot raise).
        lower_rate_per_hour: Units per hour it can remove (0 if it cannot lower).
        is_on: True while actively adjusting its variable this step.

    Raises:
        InvalidValueError: If a rate is negative or non-finite, or both are 0.
    """

    name: str
    metric: str
    raise_rate_per_hour: float = 0.0
    lower_rate_per_hour: float = 0.0
    is_on: bool = False

    def __post_init__(self) -> None:
        for label, rate in (
            ("raise_rate_per_hour", self.raise_rate_per_hour),
            ("lower_rate_per_hour", self.lower_rate_per_hour),
        ):
            _require_finite(f"{self.name}.{label}", rate)
            if rate < 0:
                raise InvalidValueError(f"{self.name}.{label} must be >= 0, got {rate}")
        if self.raise_rate_per_hour == 0 and self.lower_rate_per_hour == 0:
            raise InvalidValueError(f"{self.name} must be able to raise or lower")


@dataclass
class Zone:
    """A named grow zone with its variables and devices.

    Attributes:
        name: Unique zone name chosen by the user.
        variables: Variables keyed by name.
        devices: Equipment installed in the zone.

    Raises:
        InvalidValueError: On duplicate device names, a variable stored under
            the wrong key, or a device that targets an unknown variable.

    Complexity:
        Construction is O(V + D) time and O(D) space for the device grouping.
    """

    name: str
    variables: dict[str, Variable]
    devices: list[Device] = field(default_factory=list)
    _by_metric: dict[str, list[Device]] = field(
        default_factory=dict, init=False, repr=False
    )

    def __post_init__(self) -> None:
        for key, variable in self.variables.items():
            if key != variable.name:
                raise InvalidValueError(f"variable key {key!r} != name {variable.name!r}")
        seen: set[str] = set()
        for device in self.devices:
            if device.name in seen:
                raise InvalidValueError(f"duplicate device name {device.name!r}")
            seen.add(device.name)
            if device.metric not in self.variables:
                raise InvalidValueError(
                    f"{device.name!r} targets unknown variable {device.metric!r}"
                )
            self._by_metric.setdefault(device.metric, []).append(device)

    def device(self, name: str) -> Device:
        """Return the device called ``name``. O(D) time.

        Raises:
            InvalidValueError: If no device has that name.
        """
        for device in self.devices:
            if device.name == name:
                return device
        raise InvalidValueError(f"no device named {name!r} in zone {self.name!r}")


def step_zone(zone: Zone, hours: float = 1.0) -> Zone:
    """Advance a zone by ``hours`` of simulated time.

    For each variable, every device able to push toward the target runs, and
    the variable moves by the combined rate, stopping exactly at the target.

    Args:
        zone: Zone to update in place.
        hours: Step length in hours. Must be finite and >= 0.

    Returns:
        The same zone, for chaining.

    Raises:
        InvalidValueError: If ``hours`` is negative or not finite.

    Complexity:
        Time O(V + D), space O(1) extra, for V variables and D devices.
    """
    _require_finite("hours", hours)
    if hours < 0:
        raise InvalidValueError(f"hours must be >= 0, got {hours}")

    for variable in zone.variables.values():
        devices = zone._by_metric.get(variable.name, [])
        for device in devices:
            device.is_on = False

        error = variable.target - variable.current
        if error == 0:
            continue

        raising = error > 0
        total_rate = 0.0
        for device in devices:
            rate = device.raise_rate_per_hour if raising else device.lower_rate_per_hour
            if rate > 0:
                device.is_on = True
                total_rate += rate

        move = total_rate * hours
        if move >= abs(error):
            variable.current = variable.target  # exact, avoids float drift
        else:
            variable.current += move if raising else -move

    return zone


def build_zone(config: dict[str, Any]) -> Zone:
    """Create a Zone from plain data (dict, parsed YAML, or JSON).

    Expected shape::

        {"name": "tropical",
         "variables": {"temperature": {"unit": "F", "current": 85.0,
                                        "target": 96.9}},
         "devices": [{"name": "heater", "metric": "temperature",
                      "raise_rate_per_hour": 2.0}]}

    Raises:
        InvalidValueError: If keys are missing, unexpected, or values invalid.

    Complexity:
        Time O(V + D), space O(V + D).
    """
    try:
        variables = {
            name: Variable(name=name, **spec)
            for name, spec in config["variables"].items()
        }
        devices = [Device(**spec) for spec in config.get("devices", [])]
        return Zone(name=config["name"], variables=variables, devices=devices)
    except (KeyError, TypeError) as exc:
        raise InvalidValueError(f"invalid zone config: {exc}") from exc
