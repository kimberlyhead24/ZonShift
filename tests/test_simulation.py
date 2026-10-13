from zonshift.simulation import (
    Zone,
    Heater,
    Cooler,
    Humidifier,
    Dehumidifier,
    GrowLight,
    update_zone,
)


def create_tropical_setup():
    zone = Zone(
        name="tropical",
        current_temp_fahr=85.0,
        target_temp_fahr=96.9,
        current_humidity_perc=55.0,
        target_humidity_perc=65.0,
        current_light_ppfd=200.0,
        target_light_ppfd=500.0,
    )

    heater = Heater(
        name="tropical heater",
        zone="tropical",
        heating_rate_fahr_per_hour=2.0,
    )

    cooler = Cooler(
        name="tropical cooler",
        zone="tropical",
        cooling_rate_fahr_per_hour=2.0,
    )

    humidifier = Humidifier(
        name="tropical humidifier",
        zone="tropical",
        humidity_rate_perc_per_hour=1.5,
    )

    dehumidifier = Dehumidifier(
        name="tropical dehumidifier",
        zone="tropical",
        humidity_rate_perc_per_hour=1.5,
    )

    light = GrowLight(
        name="tropical grow light",
        zone="tropical",
        current_ppfd=200.0,
        target_ppfd=500.0,
        ppfd_step=50.0,
    )

    return zone, heater, cooler, humidifier, dehumidifier, light


def test_tropical_zone_heats_when_below_target():
    zone, heater, cooler, humidifier, dehumidifier, light = create_tropical_setup()

    update_zone(
        zone,
        heater,
        cooler,
        humidifier,
        dehumidifier,
        light,
        hours=1.0,
    )

    assert heater.is_on is True
    assert cooler.is_on is False
    assert zone.current_temp_fahr == 87.0


def test_tropical_zone_humidifies_when_below_target():
    zone, heater, cooler, humidifier, dehumidifier, light = create_tropical_setup()

    update_zone(
        zone,
        heater,
        cooler,
        humidifier,
        dehumidifier,
        light,
        hours=1.0,
    )

    assert humidifier.is_on is True
    assert dehumidifier.is_on is False
    assert zone.current_humidity_perc == 56.5


def test_tropical_zone_light_increases_toward_target():
    zone, heater, cooler, humidifier, dehumidifier, light = create_tropical_setup()

    update_zone(
        zone,
        heater,
        cooler,
        humidifier,
        dehumidifier,
        light,
        hours=1.0,
    )

    assert light.is_on is True
    assert zone.current_light_ppfd == 250.0


def test_tropical_zone_reaches_target_values():
    zone, heater, cooler, humidifier, dehumidifier, light = create_tropical_setup()

    for _ in range(10):
        update_zone(
            zone,
            heater,
            cooler,
            humidifier,
            dehumidifier,
            light,
            hours=1.0,
        )

    assert zone.current_temp_fahr == zone.target_temp_fahr
    assert zone.current_humidity_perc == zone.target_humidity_perc
    assert zone.current_light_ppfd == zone.target_light_ppfd