# ZonShift

**A simulation-first control platform for modular vertical gardens.**

Two independently configured grow zones share one thermal store, so heat
captured in one room can warm another later. Every decision is logged,
labeled and safe by default.

!!! warning "Prototype status"
    ZonShift is an early software prototype. Simulation results test control
    logic only. They are not proof of real-world energy savings, heat
    retention or crop yield.

## What it does

| Idea | In practice |
|---|---|
| Independent zones | A tropical zone and a temperate zone, each with its own targets |
| Shared thermal store | Captures excess heat and releases it when a zone needs it |
| Safety first | The server requests; the edge decides. Faults fall to a safe state |
| Honest data | Every value is labeled simulated, estimated or measured |

## Where to start

<div class="grid cards" markdown>

- :material-map-marker-path: **[Roadmap and tasks](plan.md)**

    Milestones and task cards, one issue per branch.

- :material-ruler-square: **[Conventions](conventions.md)**

    Units, naming and data labels.

- :material-vector-link: **[CRC cards](CRC.md)**

    Which class talks to which.

- :material-database-outline: **[Data model](data-model.md)**

    Dataclasses, fields and state machines.

- :material-shield-lock-outline: **[Security](security.md)**

    Threats, controls and hardening notes.

- :material-code-braces: **[API reference](api.md)**

    Generated from the docstrings.

</div>

## Run it yourself

```bash
git clone [https://github.com/kimberlyhead24/ZonShift.git](https://github.com/kimberlyhead24/ZonShift.git)
cd ZonShift
python -m pip install -r requirements-dev.txt
pytest
```

## Current status

Milestone 1 (ports, interface layer and config files) is in progress.
See the [roadmap](plan.md) for the full list.