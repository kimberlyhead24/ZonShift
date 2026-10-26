# Data model

!!! info "How to read this page"
    Each table lists a dataclass. **Unit** is the internal unit from
    [Conventions](conventions.md). Frozen means immutable after creation.

## Reading { #reading }
*Frozen. Produced by a SensorPort, consumed by Rules.*

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `zone_id` | `str` | – | Which zone was measured |
| `temp_f` | `float` | °F | Air temperature |
| `observed_at_s` | `float` | s | When it was observed, not when it arrived |
| `source` | `Source` | – | `simulated`, `estimated` or `measured` |

## ZoneConfig { #zoneconfig }
*Pydantic model, loaded with `yaml.safe_load`, `extra="forbid"`.*

| Field | Type | Unit | Rule |
|---|---|---|---|
| `zone_id` | `str` | – | Unique |
| `crop_recipe` | `str` | – | Must exist |
| `min_temp_f` | `float` | °F | Must be less than max |
| `max_temp_f` | `float` | °F | Hard limit |
| `target_temp_f` | `float` | °F | Between min and max |

## Command and Ack { #command }

| Field | Type | Meaning |
|---|---|---|
| `command_id` | `str` | Unique, used to reject replays |
| `target` | `str` | Actuator name |
| `value` | `float` | Requested setting |
| `expires_at_s` | `float` | Reject after this time |
| `Ack.status` | `AckStatus` | `accepted`, `rejected`, `expired`, `duplicate` |
| `Ack.reason` | `str` | Why it was rejected |

## ThermalStore { #thermalstore }
*Planned. Mutable state owned by the thermal bank.*

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `temp_f` | `float` | °F | Store temperature |
| `energy_kj` | `float` | kJ | Usable stored energy |
| `capacity_kj` | `float` | kJ | Maximum |
| `loss_rate_per_h` | `float` | – | Fraction lost per hour |

## State machines

=== "Thermal bank"

    ```mermaid
    stateDiagram-v2
      [*] --> Idle
      Idle --> Charging : zone has excess heat, store not full
      Idle --> Discharging : zone needs heat, store warm enough
      Charging --> Idle : store full or no excess
      Discharging --> Idle : store depleted or no demand
      Charging --> EmergencyDump : store over max temp
      Discharging --> EmergencyDump : store over max temp
      EmergencyDump --> Idle : temp back in range
    ```

=== "Command lifecycle"

    ```mermaid
    stateDiagram-v2
      [*] --> Issued
      Issued --> Accepted : valid, unexpired, unseen id
      Issued --> Rejected : unsafe or duplicate
      Issued --> Expired : expiry passed
      Accepted --> Completed : actuator confirms
      Accepted --> TimedOut : no confirmation
      Completed --> [*]
      Rejected --> [*]
      Expired --> [*]
      TimedOut --> [*]
    ```

=== "Zone safety mode"

    ```mermaid
    stateDiagram-v2
      [*] --> Normal
      Normal --> Degraded : reading missing or stale
      Degraded --> Normal : fresh reading
      Degraded --> SafeState : timeout
      Normal --> SafeState : hard limit hit
      SafeState --> Normal : operator reset and limits clear
    ```
