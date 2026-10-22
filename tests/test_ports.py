import pytest

from zonshift.adapters.sim.sensor import SimulatedSensor
from zonshift.errors import UnknownZoneError
from zonshift.ports.sensor import Quality, SensorPort


def read_temperature(sensor: SensorPort, zone_id: str) -> float:
    return sensor.read(zone_id).values["temperature"]


def test_simulated_sensor_satisfies_port(tropical_zone):
    sensor = SimulatedSensor({tropical_zone.name: tropical_zone})
    assert read_temperature(sensor, "tropical") == 85.0
    assert sensor.read("tropical").quality is Quality.SIMULATED


def test_unknown_zone_raises(tropical_zone):
    sensor = SimulatedSensor({tropical_zone.name: tropical_zone})
    with pytest.raises(UnknownZoneError):
        sensor.read("nope")