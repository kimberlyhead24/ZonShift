from dataclasses import dataclass

@dataclass
class Zone:
    name: str
    current_temp_fahr: float
    target_temp_fahr: float
    current_humidity_perc: float
    target_humidity_perc: float
    current_light_ppfd: float
    target_light_ppfd: float

@dataclass
class Device:
    name: str
    zone: str
    is_on: bool = False

@dataclass
class Heater(Device):
    heating_rate_fahr_per_hour: float = 1.0

@dataclass
class Cooler(Device):
    cooling_rate_fahr_per_hour: float = 1.0

@dataclass
class Humidifier(Device):
    humidity_rate_perc_per_hour: float = 1.0

@dataclass
class Dehumidifier(Device):
    humidity_rate_perc_per_hour: float = 1.0

@dataclass
class GrowLight(Device):
    current_ppfd: float = 0.0
    target_ppfd: float = 0.0
    ppfd_step: float = 10.0
    
tropical_zone = Zone(
    name="tropical", 
    current_temp_fahr=85.0,
    target_temp_fahr=96.9,
    current_humidity_perc=55.0,
    target_humidity_perc=65.0,
    current_light_ppfd=200.0,
    target_light_ppfd=500.0
    )

tropical_heater = Heater(
    name="tropical heater",
    zone="tropical",
    heating_rate_fahr_per_hour=2.0,
)

tropical_cooler = Cooler(
    name="tropical cooler",
    zone="tropical",
    cooling_rate_fahr_per_hour=2.0,
)

tropical_humidifier = Humidifier(
    name="tropical humidifier",
    zone="tropical",
    humidity_rate_perc_per_hour=1.5,
)

tropical_dehumidifier = Dehumidifier(
    name="tropical dehumidifier",
    zone="tropical",
    humidity_rate_perc_per_hour=1.5,
)

tropical_light = GrowLight(
    name="tropical grow light",
    zone="tropical",
    current_ppfd=200.0,
    target_ppfd=500.0,
)

def update_zone(
    zone: Zone,
    heater: Heater,
    cooler: Cooler,
    humidifier: Humidifier,
    dehumidifier: Dehumidifier,
    light: GrowLight,
    hours: float = 1.0,
) -> Zone:
    # Temperature control
    if zone.current_temp_fahr < zone.target_temp_fahr:
        heater.is_on = True
        cooler.is_on = False

        zone.current_temp_fahr = min(
            zone.current_temp_fahr + heater.heating_rate_fahr_per_hour * hours,
            zone.target_temp_fahr,
            )
        
    elif zone.current_temp_fahr > zone.target_temp_fahr:
        cooler.is_on = True
        heater.is_on = False

        zone.current_temp_fahr = max(
            zone.current_temp_fahr - cooler.cooling_rate_fahr_per_hour * hours,
            zone.target_temp_fahr,
        )
    else:
        heater.is_on = False
        cooler.is_on = False

    # Humidity control
    if zone.current_humidity_perc < zone.target_humidity_perc:
        humidifier.is_on = True
        dehumidifier.is_on = False

        zone.current_humidity_perc = min(
            zone.current_humidity_perc + humidifier.humidity_rate_perc_per_hour * hours,
            zone.target_humidity_perc,
        )
    elif zone.current_humidity_perc > zone.target_humidity_perc:
        dehumidifier.is_on = True
        humidifier.is_on = False

        zone.current_humidity_perc = max(
            zone.current_humidity_perc - dehumidifier.humidity_rate_perc_per_hour * hours,
            zone.target_humidity_perc,
        )
    else:
        humidifier.is_on = False
        dehumidifier.is_on = False

    # Light control
    if zone.current_light_ppfd < zone.target_light_ppfd:
        light.is_on = True
        zone.current_light_ppfd = min(
            zone.current_light_ppfd + light.ppfd_step * hours,
            zone.target_light_ppfd,
        )
    else:
        light.is_on = False

    return zone