import pytest

from zonshift.simulation import build_zone

TROPICAL_CONFIG = {
    "name": "tropical",
    "variables": {
        "temperature": {"unit": "F", "current": 85.0, "target": 96.9},
        "humidity": {"unit": "%", "current": 55.0, "target": 65.0,
                     "minimum": 0.0, "maximum": 100.0},
        "light": {"unit": "PPFD", "current": 200.0, "target": 500.0,
                  "minimum": 0.0},
    },
    "devices": [
        {"name": "heater", "metric": "temperature", "raise_rate_per_hour": 2.0},
        {"name": "cooler", "metric": "temperature", "lower_rate_per_hour": 2.0},
        {"name": "humidifier", "metric": "humidity", "raise_rate_per_hour": 1.5},
        {"name": "dehumidifier", "metric": "humidity", "lower_rate_per_hour": 1.5},
        {"name": "grow light", "metric": "light",
         "raise_rate_per_hour": 50.0, "lower_rate_per_hour": 50.0},
    ],
}


@pytest.fixture
def tropical_zone():
    return build_zone(TROPICAL_CONFIG)