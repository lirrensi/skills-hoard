# Testing: Resilience and Operations

> Load when uptime, load, deploy safety, observability, or disaster recovery are part of the real risk surface.

---

## Performance and Capacity

- [ ] CRITICAL IF performance matters -> THEN define pass/fail thresholds before testing: latency, throughput, error rate, saturation, and recovery expectations
- [ ] CRITICAL IF the system serves concurrent users or jobs -> THEN test load, spikes, and queueing behavior under realistic contention
- [ ] HIGH IF stateful dependencies exist -> THEN watch connection pools, memory growth, lock contention, and cache amplification under sustained load
- [ ] HIGH IF the hotspot is unknown -> THEN profile before guessing; averages are not truth, tail latency is truth
- [ ] HIGH IF the system uses autoscaling, serverless, or bursty queues -> THEN test cold start cost, backlog recovery time, and scaling limits rather than only steady-state load

---

## Chaos and Failure Recovery

- [ ] CRITICAL IF the system depends on networks, databases, queues, disks, or third-party services -> THEN test timeout, retry, circuit-breaker, and partial-failure behavior explicitly
- [ ] CRITICAL IF work spans multiple steps -> THEN test mid-operation failure and prove the system lands in a safe, recoverable state
- [ ] HIGH IF the architecture assumes idempotency or replay safety -> THEN test duplicate delivery, restart recovery, and interrupted execution
- [ ] HIGH IF the product claims graceful degradation -> THEN prove which features survive and which fail closed when dependencies disappear

---

## Observability and Operability

- [ ] CRITICAL IF the system is deployed -> THEN test health/readiness semantics, structured logs, trace propagation, and metric coverage for the golden signals
- [ ] CRITICAL IF the system handles secrets or PII -> THEN test redaction in logs, errors, traces, and alerts
- [ ] HIGH IF operators rely on alerts -> THEN run staged alert smoke checks so routing and thresholds are proven, not assumed
- [ ] HIGH IF observability pipelines can amplify failure -> THEN test log-volume spikes, trace sampling behavior, and alert flood conditions so telemetry cannot become its own outage

---

## Process and Secret Lifecycle

- [ ] CRITICAL IF the service is long-running -> THEN test startup readiness only after dependencies are actually usable, and graceful shutdown that drains or safely requeues in-flight work
- [ ] CRITICAL IF shutdown or restart can interrupt writes, jobs, or streams -> THEN prove the process exits within a bounded timeout without leaving half-finished state behind
- [ ] HIGH IF secrets, signing keys, or certificates rotate -> THEN test overlap windows, revocation, and continued decrypt or verify behavior across rotation without hidden downtime
- [ ] HIGH IF infrastructure or runtime limits are safety-critical -> THEN test disk, memory, connection-pool, and log-volume exhaustion behavior as operational failure modes

---

## Release, Rollback, and Recovery

- [ ] CRITICAL IF deploys can mix old and new versions -> THEN test compatibility during rollout across code, schema, and contract boundaries
- [ ] CRITICAL IF rollback is a supported escape hatch -> THEN test it with real state and prove it does not corrupt or orphan data
- [ ] CRITICAL IF backups matter -> THEN rehearse restore, measure recovery time and data loss window, and validate the restored system actually works
- [ ] HIGH IF infrastructure is declared as code -> THEN validate plans and scan for unsafe misconfiguration before rollout
