# Plan

!!! success "Rule"
    One task = one issue = one branch = one squash-merged PR.
    GitHub Issues is the source of truth for status.

## Workflow
1. Open an issue from a task card.
2. `git switch -c task/014-clock-port`
3. Build, test, update docs.
4. PR text says `Closes #14`; squash and merge.
5. Tick the box here and in Confluence.

## Milestones

| # | Milestone | Done when | Status |
|---|---|---|---|
| 0 | Setup and first simulation | pytest green and pushed | :material-check: Done |
| 1 | Modular refactor, ports, config | Simulator runs through both ports | :material-progress-clock: In progress |
| 2 | Thermal simulation | Store charges, discharges, loses heat | Not started |
| 3 | Event pipeline | Commands, acks and alerts flow | Not started |
| 4 | Safety and automation | Low-water, expiry, comms-loss tests pass | Not started |
| 5 | Dashboard | Zones, alerts, audit history visible | Not started |
| 6 | Energy and solar | Labeled simulated or estimated | Not started |
| 7 | Hardening and release | CI, docs, demo, security review | Not started |

!!! note "Post-MVP tracks"
    Geospatial site analysis, virtual LiDAR, aquaponics and biochar
    ideas live in the Obsidian ideas log until promoted to a card.

## Task cards, milestone 1

- [ ] **T-013 Zone config from YAML** (`safe_load`, `extra="forbid"`)
    - Learn: PyYAML safe_load, pydantic BaseModel validators
    - Done when: a bad file fails with a clear error and a test proves it
- [ ] **T-014 Clock and FakeClock** (monotonic time)
    - Learn: `time.monotonic`, dependency injection
    - Done when: tests run with no real sleeping
- [ ] **T-015 Actuator port** (replay and expiry checks)
    - Learn: `typing.Protocol`, PEP 544
    - Done when: duplicate and expired commands get a rejected Ack
- [ ] **T-016 Simulator class**
    - Done when: it satisfies both ports in a contract test
- [ ] **T-017 CI: pytest and mypy** (read-only token, pinned actions)
    - Done when: green check on a PR
