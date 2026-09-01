# 📡 IoT Domain

> **Layer 3: Domain Constraints** — *Offline-first, power constraints, unreliable network*

## Domain Constraints → Design Implications

| Domain Rule | Design Constraint | Rust Implication |
|-------------|-------------------|------------------|
| Unreliable network | Offline-first design | Local buffering |
| Power constraints | Efficient code | Sleep modes, minimal allocation |
| Resource limits | Small footprint | `no_std` where needed |
| Security | Encrypted comms | TLS, signed firmware |
| Reliability | Self-recovery | Watchdog, error handling |
| OTA updates | Safe upgrades | Rollback capability |

## Critical Constraints

### Network Unreliability

```
RULE: Network can fail at any time
WHY: Wireless, remote locations
RUST: Local queue, retry with backoff
```

### Power Management

```
RULE: Minimize power consumption
WHY: Battery life, energy costs
RUST: Sleep modes, efficient algorithms
```

### Device Security

```
RULE: All communication encrypted
WHY: Physical access possible
RUST: TLS, signed messages
```

## Environment Comparison

| Environment | Stack | Crates |
|-------------|-------|--------|
| Linux gateway | `tokio` + std | `rumqttc`, `reqwest` |
| MCU device | `embassy` + `no_std` | `embedded-hal` |
| Hybrid | Split workloads | Both |

## Key Crates

| Purpose | Crate |
|---------|-------|
| MQTT | `rumqttc`, `rumqttd` |
| CoAP | `coap-lite` |
| HTTP | `reqwest` |
| Async embedded | `embassy` |
| Embedded HAL | `embedded-hal` |

## Common Mistakes in IoT Domain

- Not buffering data for offline scenarios
- Blocking in low-power mode
- No watchdog timer
- Unencrypted communication
- No retry/backoff for network operations

## Related References

- [07-concurrency](../references/07-concurrency.md) — async with timeout
- [06-error-handling](../references/06-error-handling.md) — retry with backoff
- [13-lifecycle](../references/13-lifecycle.md) — local buffer persistence
