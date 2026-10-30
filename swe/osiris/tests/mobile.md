# Testing: Mobile

> Load when the repo ships a native, React Native, Flutter, Capacitor, or otherwise mobile-specific app surface.

---

## Device and Lifecycle Behavior

- [ ] CRITICAL IF the app can background, foreground, suspend, or resume -> THEN test lifecycle transitions for crashes, duplicate work, and lost state
- [ ] CRITICAL IF network connectivity is unreliable -> THEN test offline behavior, reconnect sync, queue replay, and stale-state handling
- [ ] HIGH IF memory, battery, or startup time matter -> THEN test cold start, warm resume, and degraded-device behavior rather than only ideal simulators
- [ ] HIGH IF requests can be interrupted by app state or network shifts -> THEN test mid-request offline or online transitions, duplicate submit on reconnect, and safe recovery after OS process death

---

## Platform Integrations

- [ ] CRITICAL IF the app requests permissions -> THEN test first prompt, denial, revocation from settings, and partial permission states
- [ ] CRITICAL IF deep links or universal links exist -> THEN test routing into the correct screen with valid, invalid, expired, and unauthorized targets
- [ ] HIGH IF push notifications exist -> THEN test receipt, tap-through navigation, background behavior, and duplicate-delivery protection
- [ ] HIGH IF camera, files, location, contacts, or sensors are used -> THEN test unavailable hardware, revoked permissions, and malformed returned data

---

## Mobile UX Risk

- [ ] HIGH IF forms or interactive screens are important -> THEN test keyboard overlap, focus movement, rotation, and small-screen layout behavior
- [ ] MEDIUM IF multiple OS versions are supported -> THEN test the minimum supported version, not only the newest one
- [ ] MEDIUM IF localization exists -> THEN test long strings, RTL, and native formatting differences on real device classes

## Device and OS Matrix

- [ ] HIGH IF multiple devices or OS versions matter -> THEN test minimum supported OS and smallest screen class, not only the newest flagship
- [ ] MEDIUM IF behavior differs by vendor or OS -> THEN pin the matrix (OS range, device classes, input modes) and run critical journeys on each leg

## Upgrade and Install Lifecycle

- [ ] HIGH IF the app stores local data -> THEN test upgrade over an old version: schema migration, session survival, no data loss
- [ ] MEDIUM IF install or reinstall flows exist -> THEN test fresh install, reinstall over existing data, and uninstall leftovers

## Push and Deep-Link Payloads

- [ ] HIGH IF push exists -> THEN test malformed, oversized, and stale payloads; tap-through to correct, expired, and unauthorized targets
- [ ] HIGH IF deep links exist -> THEN test untrusted link payloads for injection into routing, params, and auth state

## Network Conditions and Power

- [ ] HIGH IF the app runs on real networks -> THEN test on slow, lossy, and switching networks (Wi-Fi ↔ cellular), not only ideal connectivity
- [ ] MEDIUM IF background work exists -> THEN test OS throttling, battery-saver mode, and background-execution limits
