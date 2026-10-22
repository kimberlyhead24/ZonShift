import pytest

from zonshift.errors import InvalidValueError
from zonshift.simulation import build_zone, step_zone


def test_heats_when_below_target(tropical_zone):
    step_zone(tropical_zone, hours=1.0)
    assert tropical_zone.device("heater").is_on is True
    assert tropical_zone.device("cooler").is_on is False
    assert tropical_zone.variables["temperature"].current == 87.0


def test_humidifies_when_below_target(tropical_zone):
    step_zone(tropical_zone, hours=1.0)
    assert tropical_zone.device("humidifier").is_on is True
    assert tropical_zone.device("dehumidifier").is_on is False
    assert tropical_zone.variables["humidity"].current == 56.5


def test_light_ramps_up(tropical_zone):
    step_zone(tropical_zone, hours=1.0)
    assert tropical_zone.device("grow light").is_on is True
    assert tropical_zone.variables["light"].current == 250.0


def test_light_ramps_down():
    zone = build_zone({
        "name": "z",
        "variables": {"light": {"unit": "PPFD", "current": 500.0,
                                "target": 200.0, "minimum": 0.0}},
        "devices": [{"name": "lamp", "metric": "light",
                     "raise_rate_per_hour": 50.0, "lower_rate_per_hour": 50.0}],
    })
    step_zone(zone, hours=1.0)
    assert zone.variables["light"].current == 450.0


def test_reaches_all_targets(tropical_zone):
    for _ in range(10):
        step_zone(tropical_zone, hours=1.0)
    for variable in tropical_zone.variables.values():
        assert variable.current == variable.target


def test_custom_zone_with_new_variable():
    zone = build_zone({
        "name": "co2-room",
        "variables": {"co2": {"unit": "ppm", "current": 400.0, "target": 800.0}},
        "devices": [{"name": "injector", "metric": "co2",
                     "raise_rate_per_hour": 100.0}],
    })
    step_zone(zone, hours=2.0)
    assert zone.variables["co2"].current == 600.0


def test_negative_hours_rejected(tropical_zone):
    with pytest.raises(InvalidValueError):
        step_zone(tropical_zone, hours=-1.0)


def test_value_outside_limits_rejected():
    with pytest.raises(InvalidValueError):
        build_zone({"name": "z", "variables": {"humidity": {
            "unit": "%", "current": 140.0, "target": 60.0,
            "minimum": 0.0, "maximum": 100.0}}})


def test_device_with_unknown_variable_rejected():
    with pytest.raises(InvalidValueError):
        build_zone({"name": "z",
                    "variables": {"temperature": {"unit": "F", "current": 70.0, "target": 70.0}},
                    "devices": [{"name": "fan", "metric": "wind", "raise_rate_per_hour": 1.0}]})


def test_duplicate_device_names_rejected():
    spec = {"name": "fan", "metric": "temperature", "lower_rate_per_hour": 1.0}
    with pytest.raises(InvalidValueError):
        build_zone({"name": "z",
                    "variables": {"temperature": {"unit": "F", "current": 70.0, "target": 70.0}},
                    "devices": [spec, spec]})