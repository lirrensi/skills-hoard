# Testing: Frontend

> Load when the repo renders interactive UI in a browser or desktop shell.

---

## Component and View Behavior

- [ ] CRITICAL IF a component renders conditionally -> THEN test each meaningful branch: loading, empty, success, error, disabled, unauthorized, and stale states where relevant
- [ ] CRITICAL IF user interaction changes state -> THEN test click, type, submit, keyboard, focus, and callback behavior with assertions on visible outcome
- [ ] CRITICAL IF components fetch or depend on async data -> THEN prove transitions between pending, fulfilled, partial, and failed states
- [ ] HIGH IF rendering depends on props or context -> THEN test wrong, missing, and surprising values rather than only the ideal case
- [ ] HIGH IF lists or collections render -> THEN test empty, single-item, many-item, and duplicate-key edge cases

---

## State, Routing, and Client Logic

- [ ] CRITICAL IF the app has shared client state -> THEN test reducers, stores, selectors, and side effects as behavior, not as implementation trivia
- [ ] HIGH IF routes or deep links exist -> THEN test direct entry, redirect, unauthorized access, and back/forward navigation behavior
- [ ] HIGH IF feature flags, persisted state, caching, or time-based UI logic exist -> THEN test both enabled and disabled states plus rehydration and expiry boundaries
- [ ] HIGH IF forms or navigation can be repeated accidentally -> THEN test resubmission guards, unsaved-changes prompts, and scroll restoration instead of assuming ideal user behavior
- [ ] MEDIUM IF localization exists -> THEN test long strings, RTL behavior, and locale-sensitive formatting where layout or meaning can break

---

## Session and Browser Storage

- [ ] CRITICAL IF the UI participates in auth or long-lived sessions -> THEN test session expiry, refresh-token rotation, remember-me behavior, and logout cleanup across cookies, storage, and in-memory state
- [ ] HIGH IF auth state can exist in multiple tabs or windows -> THEN test login, logout, and token-refresh propagation so one tab cannot silently drift from another
- [ ] HIGH IF browser storage persists client state -> THEN test stale schema migration and corrupted storage recovery so the app degrades safely instead of white-screening
- [ ] MEDIUM IF forms depend on browser capabilities such as autofill, clipboard, drag-and-drop, or password managers -> THEN verify the app still behaves safely and predictably

---

## Accessibility and Safety

- [ ] CRITICAL IF the UI is interactive -> THEN verify keyboard reachability, visible focus, label associations, and error announcement behavior
- [ ] HIGH IF dialogs, menus, or overlays exist -> THEN test focus trapping, escape handling, dismissal rules, and restoration of focus
- [ ] HIGH IF user content is rendered -> THEN test escaping and sanitization so the UI does not become an XSS delivery surface
- [ ] CRITICAL IF the UI is interactive -> THEN meet WCAG 2.2 AA: contrast 4.5:1 text / 3:1 UI, visible focus, keyboard-only path, 200% zoom with reflow, reduced-motion respected
- [ ] CRITICAL IF forms exist -> THEN announce and associate every error, never use placeholder-only labels, move focus to the first error
- [ ] HIGH IF a critical flow ships -> THEN run an automated axe pass plus one manual keyboard pass per flow

---

## Visual Stability

- [ ] HIGH IF stable components or pages have historically regressed visually -> THEN add focused visual or snapshot checks for those surfaces
- [ ] HIGH IF using snapshots -> THEN keep them small, intentional, and reviewable; never snapshot an entire changing page as a rubber stamp
- [ ] MEDIUM IF responsive layout matters -> THEN test key viewports instead of assuming desktop success means mobile success

## Browser and Device Matrix

- [ ] HIGH IF the UI ships to browsers or devices -> THEN define the supported matrix: browsers, viewports, input modes; test minimum supported, not only latest
- [ ] HIGH IF journeys are critical -> THEN run cross-browser checks on those journeys, not only the default browser

## Async UI and Network

- [ ] CRITICAL IF concurrent requests can race -> THEN test race and last-write-wins behavior explicitly
- [ ] HIGH IF the UI works offline or on flaky networks -> THEN test retry, offline, and reconnect behavior
- [ ] HIGH IF optimistic updates exist -> THEN test optimistic apply, server rejection rollback, and cancellation
- [ ] MEDIUM IF caching or revalidation exists -> THEN test stale-while-revalidate: stale shown, fresh swapped, no flicker to empty
