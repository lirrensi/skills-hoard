---
name: docker-best-practices
description: Harden Docker Compose services for real servers by adding resource limits, restart policy, log rotation, health checks, and volume backup plans. Use whenever the user asks to review or write docker-compose.yml/compose.yaml for production, self-hosting, homelab/server deployment, Docker reliability, container hardening, or why a Compose stack dies overnight, fills the disk, or starts in the wrong order.
---

# docker-best-practices

Turn a cute local `compose.yaml` into something less likely to faceplant on a real server.

## Platform

- Primary target: Linux Docker hosts with `docker compose`
- Works for homelabs, VPSes, and single-host self-hosted stacks
- Windows/macOS are fine for editing, but host-side validation commands here are Linux-first

## What this skill is for

Use this skill when the user wants to:

- harden a Compose stack before deployment
- review an existing `docker-compose.yml` or `compose.yaml`
- stop one container from eating the whole box
- make services restart after crashes
- stop Docker JSON logs from colonizing the disk
- make startup wait for healthy dependencies
- avoid losing data from named volumes with zero backup plan

## Quick scout

Check the Compose file and the host basics first:

```bash
docker compose version
docker compose config
docker info
```

Modern Compose note: omit the old top-level `version:` field unless the user has a very specific legacy reason.

If the stack already exists, inspect the current pain points:

```bash
docker compose ps
docker stats --no-stream
du -sh /var/lib/docker/containers/*/*-json.log | sort -h
```

## Workflow

1. Identify which services are stateless vs stateful.
2. Add memory and CPU guardrails so one container cannot bully the host.
3. Set an explicit restart policy for long-running services.
4. Add log rotation to every chatty service.
5. Add health checks for the app and critical dependencies.
6. Use `depends_on` with `service_healthy` or `service_completed_successfully` where startup ordering matters.
7. Audit named volumes and define a backup path for anything that matters.
8. Validate the rendered Compose config and inspect the running containers.

## Out of scope

- Full Dockerfile optimization belongs in a Dockerfile-focused skill.
- Kubernetes, Swarm, and cloud orchestrators are different beasts.
- This skill is for single-host Compose reliability and production hygiene.

## The five production defaults people forget

### 1) Resource limits

Set ceilings for memory and CPU. Current Docker Compose supports `deploy.resources` for local Compose too, so use it unless the user's environment proves otherwise.

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "1.0"
        reservations:
          memory: 256M

  postgres:
    deploy:
      resources:
        limits:
          memory: 1G
```

- `limits` = hard ceiling
- `reservations` = intended minimum
- If a container exceeds its memory limit, it can be OOM-killed inside its cgroup instead of taking neighbors down with it

Useful check:

```bash
docker inspect CONTAINER --format='{{.State.OOMKilled}}'
```

For Postgres, size `shared_buffers` with the container memory limit in mind.

### 2) Restart policy

Never leave long-running services on the default `restart: "no"` unless you truly mean it.

```yaml
services:
  app:
    restart: unless-stopped
```

- Prefer `unless-stopped` for normal services
- Use `on-failure` or `"no"` for one-shot jobs like migrations or data seeds

Example with gated migration:

```yaml
services:
  migrator:
    image: myapp:latest
    command: ["python", "manage.py", "migrate"]
    restart: "no"

  app:
    restart: unless-stopped
    depends_on:
      migrator:
        condition: service_completed_successfully
```

### 3) Log rotation

Docker's `json-file` logs will happily become a disk-eating gremlin if you let them.

```yaml
services:
  app:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

- Good default: 10 MB × 3 files per container
- Increase only if the user truly needs more on-host history
- If the whole host should default to rotation, mention `/etc/docker/daemon.json`

Useful check:

```bash
du -sh /var/lib/docker/containers/*/*-json.log | sort -h
```

### 4) Health checks and startup ordering

Running is not the same as healthy. A PID can exist while the app is spiritually deceased.

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s

  postgres:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

Then gate service startup:

```yaml
services:
  app:
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
```

Important nuance: health checks help Compose wait on dependencies, but they do **not** by themselves restart an unhealthy container. Restart behavior comes from the restart policy handled by the Docker Engine.

If the image lacks `curl`, a shell probe is fine:

```yaml
healthcheck:
  test: ["CMD-SHELL", "wget -q --spider http://localhost:8080/health || exit 1"]
```

### 5) Backups for named volumes

If the data matters, `volumes:` is not a backup strategy. It's just persistence on the same host.

```yaml
volumes:
  pgdata:
```

For a simple Postgres backup sidecar:

```yaml
services:
  backup:
    image: postgres:16-alpine
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./backups:/backups
    entrypoint: >
      sh -c "while true; do
        PGPASSWORD=$$POSTGRES_PASSWORD pg_dump -h postgres -U postgres mydb |
        gzip > /backups/backup_$$(date +%Y%m%d_%H%M%S).sql.gz;
        find /backups -mtime +7 -delete;
        sleep 86400;
      done"
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    restart: unless-stopped
```

- Local backup folder protects against `docker compose down -v`
- Off-host sync protects against host death
- For Redis used only as a cache, backup may be unnecessary; for real data, enable persistence and back it up too

## Small extras that punch above their weight

These are not the main five, but they catch a lot of real-world nonsense fast:

- pin images to a real tag instead of `latest`
- do not store secrets directly in the Compose file when env files or secrets are available
- expose only the ports that truly need host access
- consider `read_only: true`, `tmpfs`, or dropped capabilities for internet-facing services
- use override files or profiles for dev-only tooling instead of dragging it into prod
- add `init: true` for processes that spawn children badly and otherwise leak zombies
- set `stop_grace_period` when the app or database needs real shutdown time

Example runtime hardening for a simple service:

```yaml
services:
  app:
    init: true
    stop_grace_period: 30s
    read_only: true
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
```

Use this carefully:

- `read_only: true` is lovely until the app tries to write caches, PID files, uploads, or temp files into the image filesystem
- `cap_drop: [ALL]` is great for many web apps, but some services genuinely need extra capabilities
- `init: true` helps signal handling and child process cleanup; it is a tiny setting with suspiciously large emotional impact

## Service aliveness mini-checklist

Apply this per important service, especially app, database, queue, reverse proxy, and backup jobs.

### Long-running service

- has explicit `restart:`
- has meaningful `healthcheck:`
- has resource limits
- has log rotation
- exposes only intended ports
- has persistent storage only if it truly needs it

### Stateful service

- volume path is explicit and intentional
- memory limit is realistic for the service
- shutdown is graceful enough to flush data
- backup path exists
- backup retention exists
- backup is copied off-host if the data matters

### One-shot job

- uses `restart: "no"` or `on-failure`
- is gated with `service_completed_successfully` where appropriate
- failure blocks dependent services instead of silently continuing

## Common gotchas that bite people at 2 a.m.

### `depends_on` is not magic readiness without conditions

Plain `depends_on` controls start order, not actual readiness. If the database container starts but is still booting, the app can still die immediately.

Prefer:

```yaml
depends_on:
  postgres:
    condition: service_healthy
```

### Health check success must mean the service is usable

Bad health checks only prove that a shell command exists or that a port answers. That is fake comfort.

- good app check: `/health` or `/ready` endpoint returning success only when dependencies are ready enough
- good DB check: native probe such as `pg_isready`
- bad check: `echo ok`, `true`, or an endpoint that always returns 200 even while the app is broken inside

### `localhost` inside a container is the container itself

If one container tries to reach another with `localhost`, it is talking to itself like a confused golden retriever.

- use the service name on the Compose network, like `postgres`, `redis`, or `app`
- use `localhost` only for processes inside the same container

### Bind mounts can hide files baked into the image

If the image contains app files at `/app` and production mounts `./:/app`, the mount wins and the image contents are hidden.

- great for dev hot reload
- dangerous in prod when the host path is incomplete, wrong, or permission-weird

### `docker compose down -v` removes named volumes

That flag is not a cute cleanup command for stateful apps. It is data deletion with better branding.

- mention this explicitly when the stack contains databases
- prefer backups before cleanup

### `latest` is not a version strategy

Using `latest` makes rollbacks, incident review, and reproducibility all nastier than they need to be.

- prefer explicit versions like `postgres:16-alpine`
- when possible, pin even tighter if change control matters

### Secrets in `environment:` are easy to leak

Environment variables are common and practical, but they also show up in many places: shell history, CI logs, process inspection, copied config snippets, and support screenshots.

- keep secrets out of committed Compose files
- use `.env`, secret stores, or Docker secrets where practical
- never paste real credentials into examples returned to the user

### `container_name` can backfire

Hard-coding `container_name` feels tidy until you want multiple copies of the stack, project-name isolation, or cleaner automation.

- avoid it unless the user has a very specific operational need
- let Compose name containers predictably from project and service

### Profiles are for optional services, not silent prod drift

Profiles are great for admin UIs, debug tools, seed helpers, and dev extras.

- keep production-critical services outside optional profiles
- document which profiles are expected in each environment

### Graceful shutdown matters more than people think

Some services need time to flush buffers, finish requests, or close DB writes.

```yaml
services:
  app:
    stop_grace_period: 30s
```

If the app ignores signals or exits violently, restarts and updates become much messier.

## Quick review flow for an existing Compose file

When the user asks for a review, move in this order:

1. Render with `docker compose config` so merges, env interpolation, and profiles are visible.
2. Mark each service as long-running, one-shot, or stateful.
3. Check the five core settings first.
4. Scan for gotchas: `latest`, `localhost`, bind mounts in prod, `container_name`, no shutdown grace, no backups.
5. Return only the highest-risk fixes first if the stack is messy.

## Fast anti-pattern scan

Flag these immediately during review:

- `image: something:latest`
- app container using `localhost` for another service
- no memory limits on databases, app servers, or queues
- no restart policy on long-running services
- no log rotation on chatty services
- fake or useless health checks
- bind mounts or debug tooling copied straight from dev into prod
- fixed `container_name` with no real reason
- stateful services with no shutdown grace period
- named volumes holding real data with no backup destination

## Opinionated review checklist

When reviewing a Compose file, explicitly answer:

- Which services have memory limits?
- Which services have CPU limits?
- Which long-running services have restart policy?
- Which services rotate logs?
- Which services expose a meaningful health check?
- Which services need `init: true` or `stop_grace_period`?
- Which dependencies are gated on `service_healthy`?
- Which one-shot tasks use `service_completed_successfully`?
- Which named volumes hold real data?
- Where do backups go, and are they copied off-host?
- Are any images pinned poorly with `latest`?
- Is any service using `localhost` to reach a different container?
- Are secrets or dev-only mounts leaking into production?

## Validate

Render the final config:

```bash
docker compose config
```

Bring it up and inspect evidence:

```bash
docker compose up -d
docker compose ps
docker compose logs --tail=100
docker inspect CONTAINER --format='{{json .HostConfig.RestartPolicy}}'
docker inspect CONTAINER --format='{{json .State.Health}}'
docker inspect CONTAINER --format='{{.State.OOMKilled}}'
```

Reality checks:

- confirm every critical service has the intended restart policy
- confirm health status is actually `healthy`, not just `running`
- confirm services can reach each other by service name, not accidental localhost assumptions
- confirm log files are bounded
- confirm stateful services have backup output appearing where expected

## Troubleshooting cues

- Service is `running` but broken: missing or weak health check
- App starts before DB: add `depends_on` with `service_healthy`
- App says connection refused to `localhost`: it probably meant the other service name on the Compose network
- Container restarts forever: the restart policy is working; the app is still crashing, so read logs
- Service dies on shutdown or corrupts writes: increase `stop_grace_period` and verify signal handling
- Disk fills anyway: rotation may be missing on some services, or Docker daemon defaults are not applied to old containers
- Postgres still gets murdered: memory limit is too low, query load is too high, or DB tuning ignores the container limit
- Backup exists only on the same host: still one hardware failure away from crying in production

## Output

Return:

- a hardened Compose snippet or patch
- the five settings you added or verified
- any risky gaps still left open
- validation commands to run next
- gotchas the user should watch during future changes
- one short backup note for stateful services

## Notes

- This skill is about single-host Docker Compose hardening, not full Kubernetes design.
- Prefer explicit reliability settings over default behavior.
- If the user already has application-level retry logic, keep it; health-gated startup still helps.
- Do not pretend a named volume is a backup. That is just storage wearing a fake moustache.
