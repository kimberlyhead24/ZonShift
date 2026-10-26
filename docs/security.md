# Security

!!! warning "Principle"
    The server **requests**; the edge **decides**. Every layer fails to a safe state.

## Threats and controls

| Asset | Threat | Control | Task |
|---|---|---|---|
| Config files | Malicious YAML runs code | `yaml.safe_load`, pydantic `extra="forbid"` | T-013 |
| Commands | Replay or stale command | Unique ID, expiry, seen-ID set | T-015 |
| Time | Clock tampering | Monotonic clock for expiry | T-014 |
| CI | Token abuse | `permissions: contents: read`, pinned actions | T-017 |
| Secrets | Leaked keys | `.env` ignored, secret scanning on | all |
| MQTT | Anonymous clients, snooping | Auth, topic ACLs, TLS | later |
| Django | Weak settings | `check --deploy`, env-based secret key | later |
| Firmware | Overflow, hung loop | Bounds checks, watchdog, safe state | later |

## Standard practice checklist
- No secrets in the repo; read them from environment variables.
- No anonymous writes; roles with least privilege.
- Lockouts: limit failed attempts, back off, require a reset for hardware faults.
- Encrypt in transit (TLS) and at rest; use vetted libraries only.
- Log every command and decision for audit.

## Later-stage notes
Moved here from Obsidian as each becomes a task.
