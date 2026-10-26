# Conventions

!!! info "One rule"
  Every value has **one internal unit**. Convert only at the edges
  (config files, sensors, UI).

## Units

| Quantity | Internal unit | Field suffix | Example |
|---|---|---|---|
| Temperature | Fahrenheit | `_f` | `temp_f` |
| Time | seconds (monotonic) | `_s` | `expiry_s` |
| Light | PPFD, umol/m2/s | `_ppfd` | `light_ppfd` |
| Energy | kWh (electric), kJ (thermal) | `_kwh`, `_kj` | `stored_kj`|

!!! warning "Temperatures differences"
  Heat math (kJ per degree) uses a *difference*. One degree F is 5/9 of
  a degree C, so convert the difference with `delta_c = delta_f * 5/9`.
  Never convert with the +32 offset for differences.

## Naming
- Unit alwas in the name: `target_temp_f`, not `target`.
- Ports end in `Port`.

## Data labels
Every reading carries `source`: `simulated`, `estimated` or `measured`.
