# ZonShift

ZonShift is a simulation-first prototype for a modular vertical-garden monitoring and control platform. It is designed to explore how independently configured grow zones can share heating and cooling resources through a common thermal store.


ZonShift Vertical Farming Software
Copyright (C) 2026  Kimberly Head

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by  the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
Licensed under GPL-3.0-or-later

## Project goal

Build a prototype that demonstrates:

- Two simulated grow zones with independently configured temperature targets
- Coordinated heating and cooling decisions
- A shared thermal store that captures excess heat for later use
- Control behavior under changing demand, storage limits, and equipment availability
- Energy accounting that distinguishes electrical consumption from thermal energy transferred

## Current status

This is an early development milestone. The repository currently contains the initial simulation structure and automated tests.

The first implementation focuses on a small, testable core:

- A tropical grow zone
- A temperate grow zone
- A shared thermal-storage model
- Basic control logic
- Pytest-based validation

## Scope

The minimum viable product simulates two grow zones and one shared thermal store. Underground thermal storage is a future implementation option, not part of the initial simulation.

Simulation results are intended to support software design and control-logic validation. They are not presented as proof of physical performance, seasonal heat retention, or real-world energy savings.

## Technology

- Python
- Pytest for automated testing
- GitHub Codespaces for cloud-based development and testing

## Getting started

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the tests:

```bash
pytest
```

## Roadmap

- [x] Create repository structure
- [x] Add initial simulation module
- [x] Add first automated test
- [ ] Model zone heating and cooling demand
- [ ] Add shared thermal-storage behavior
- [ ] Implement controller decision logic
- [ ] Add safety and fault-condition tests
- [ ] Add energy accounting
- [ ] Add a simple dashboard
- [ ] Evaluate a small physical hardware prototype

## Documentation

Detailed project planning and design notes are maintained in Confluence. This repository contains the working code, tests, and implementation history.
