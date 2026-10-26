# About

## Why ZonShift exists

Small farms often run heating, cooling, lighting, irrigation and energy as
separate systems. ZonShift explores one coordinated approach. Zones are
configured independently, share a thermal store, and make their energy use
and equipment decisions visible and auditable.

## Design principles

1. **Simulation first.** Prove the control logic in software before spending
   money on hardware.
2. **Ports and adapters.** The core talks to interfaces. A simulator or real
   hardware plugs in behind them.
3. **The edge decides.** A server can request an action, but the local
   controller checks whether it is safe.
4. **Fail safe.** A missing reading, expired command or lost link leads to a
   safe state, never an open valve or full lights.
5. **Label everything.** Data is marked simulated, estimated or measured.

## Scope

=== "In scope"

    - Two simulated zones and one shared thermal store
    - Safety logic, alerts and energy accounting
    - Automated tests and reproducible setup
    - Interfaces ready for real sensors and actuators

=== "Not in scope"

    - Production-scale HVAC or high-voltage equipment
    - Automated nutrient dosing
    - Claims of certification or unattended operation
    - Proof of physical performance

## Technology

!!! note "Proposed, not final"
    These are the planned directions and may change as the design matures.

| Layer | Technology | Role |
|---|---|---|
| Core and simulation | Python | Logic, tests, simulator |
| Operator pages | Django | Accounts, roles, config, audit history |
| Automation service | FastAPI | Telemetry, rules, alerts, command API |
| Edge control | C++ | Sensors, limits, actuators |
| Messaging | MQTT (Mosquitto) | Decoupled telemetry and commands |
| Storage | PostgreSQL | Durable data |

## Project links

- [GitHub repository](https://github.com/kimberlyhead24/ZonShift)
- Project plan: add your public Confluence link here after you publish the page.

## License and author

Copyright (C) 2026 Kimberly Head. Released under
GPL-3.0-or-later. See the `LICENSE` file for the full terms.