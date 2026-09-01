# General Application Extraction Patterns

Patterns for extracting setup, configuration, and operational knowledge from
application-style repositories. Used in Phase 3C of the git-to-skill pipeline.

This is the default/fallback extraction strategy for any repo that doesn't clearly
fit CLI Tool or Library categories.

---

## Extraction Focus Areas

### 1. Setup & Configuration

**Source files to inspect:**

| File                  | What to extract                                           |
| --------------------- | --------------------------------------------------------- |
| `.env.example`        | All environment variables, their purposes, default values |
| `config/` directory   | Available config files, formats, documentation            |
| `docker-compose.yml`  | Services, ports, volumes, environment, dependencies       |
| `Dockerfile`          | Base image, build stages, exposed ports, entrypoint       |
| `Makefile`            | Setup targets (`make install`, `make setup`)              |
| `package.json`        | Scripts section (start, build, dev, test)                 |
| `pyproject.toml`      | Scripts and dependency groups                             |
| `README.md`           | "Installation" or "Getting Started" section               |
| `docs/install.md`     | Platform-specific install instructions                    |
| `setup.sh`            | Existing setup script (reference, don't duplicate)        |

**Environment variable extraction pattern:**
```yaml
env_vars:
  - name: DATABASE_URL
    description: "PostgreSQL connection string"
    required: true
    default: null
    format: "postgresql://user:pass@host:port/db"
  - name: PORT
    description: "HTTP server port"
    required: false
    default: "3000"
    format: numeric
  - name: LOG_LEVEL
    description: "Logging verbosity"
    required: false
    default: "info"
    values: ["debug", "info", "warn", "error"]
```

**Config file extraction pattern:**
```yaml
config_files:
  - path: "config.yaml"
    format: yaml
    required: false
    sections:
      - name: server
        fields:
          - name: host
            type: string
            default: "0.0.0.0"
          - name: port
            type: integer
            default: 8080
```

---

### 2. Operations & Dev Workflow

**Source files to inspect:**

| File                   | What to extract                                     |
| ---------------------- | --------------------------------------------------- |
| `Makefile`             | Build, test, lint, clean targets                    |
| `package.json scripts` | `dev`, `build`, `start`, `test`, `lint`, `format`   |
| `.github/workflows/`   | CI/CD pipeline steps (build → test → deploy)        |
| `.dockerignore`        | What's excluded from Docker builds                  |
| `docker-compose.yml`   | How services connect, ports, volumes                |
| `Procfile`             | Process types and run commands                       |
| `fly.toml`             | Deployment configuration                             |
| `systemd/`             | Service unit files                                   |
| `.gitlab-ci.yml`       | GitLab CI pipeline                                   |
| `Taskfile.yml`         | Task definitions                                     |
| `Justfile`             | Just task runner commands                            |
| `README.md`            | "Development" section                                |
| `CONTRIBUTING.md`      | Dev setup and contribution workflow                  |

**Operational workflow extraction:**
```markdown
## Development

### Prerequisites
- <language> <version>
- <database> <version>
- <other services>

### Setup
```bash
# Clone and install
git clone <repo>
cd <repo>
<package-manager> install
cp .env.example .env
# Edit .env with your values
```

### Run (Development)
```bash
<dev command>
```

### Build
```bash
<build command>
```

### Test
```bash
<test command>
# With coverage:
<coverage command>
```

### Lint / Format
```bash
<lint command>
<format command>
```

### Debug
```bash
# Set log level:
LOG_LEVEL=debug <run command>
# Or use:
<debug command>
```

### Docker
```bash
docker compose up -d
docker compose logs -f
docker compose down
```
```

---

### 3. Architecture Overview

**Source files to inspect:**

| File / Dir            | What to extract                                    |
| --------------------- | -------------------------------------------------- |
| Top-level directory   | Module organization, naming conventions            |
| `src/`, `lib/`, `app/`| Source code structure and layering                 |
| `README.md`           | Architecture description (if present)              |
| `docs/arch/`          | Architecture Decision Records (ADRs)               |
| `docs/`               | Additional documentation files                     |
| `api/`                | API route definitions                              |
| `db/`, `migrations/`  | Database schema and migration strategy             |
| `graphql/`, `schema/` | GraphQL schema definitions                         |
| OpenAPI/Swagger files | REST API documentation                             |

**Architecture output format:**
```markdown
## Architecture

### Directory Structure
```
src/
├── api/          # HTTP handlers / routes
├── domain/       # Business logic
├── infrastructure/ # External services, database, cache
├── config/       # Configuration loading
└── main.ts       # Application entry point
```

### Key Components
| Component    | Responsibility                        | Location            |
| ------------ | ------------------------------------- | ------------------- |
| API Layer    | HTTP request handling, validation     | `src/api/`          |
| Domain       | Business logic, rules                 | `src/domain/`       |
| Database     | Data persistence (PostgreSQL)         | `src/infrastructure/db/` |
| Cache        | Session/rate-limit storage (Redis)    | `src/infrastructure/cache/` |

### Data Flow
1. HTTP request → API Layer (validation)
2. API Layer → Domain (business logic)
3. Domain → Infrastructure (data access)
4. Response flows back through the chain

### External Dependencies
| Service    | Purpose            | Required | Connection       |
| ---------- | ------------------ | -------- | ---------------- |
| PostgreSQL | Primary database   | yes      | `DATABASE_URL`   |
| Redis      | Caching / sessions | no       | `REDIS_URL`      |
| S3         | File storage       | no       | `AWS_*` env vars |
```

If an OpenAPI/Swagger spec is present, generate an API endpoint reference table:

```markdown
### API Endpoints

| Method | Path                     | Description              |
| ------ | ------------------------ | ------------------------ |
| GET    | `/api/v1/users`          | List users               |
| POST   | `/api/v1/users`          | Create user              |
| GET    | `/api/v1/users/:id`      | Get user by ID           |
| PUT    | `/api/v1/users/:id`      | Update user              |
| DELETE | `/api/v1/users/:id`      | Delete user              |
| POST   | `/api/v1/auth/login`     | Authenticate             |
| GET    | `/api/v1/health`         | Health check             |
```

---

### 4. Deployment

**Source files to inspect:**

| File              | What to extract                               |
| ----------------- | --------------------------------------------- |
| `Dockerfile`      | Build instructions, multi-stage setup         |
| `.github/workflows/deploy.yml` | Deployment pipeline               |
| `k8s/`, `kube/`   | Kubernetes manifests (deployments, services)  |
| `helm/`           | Helm charts                                   |
| `terraform/`      | Infrastructure as code                        |
| `ansible/`        | Ansible playbooks                             |
| `serverless.yml`  | Serverless framework config                   |
| `vercel.json`     | Vercel deployment config                      |
| `netlify.toml`    | Netlify deployment config                     |
| `fly.toml`        | Fly.io deployment config                      |

**Deployment output format:**
```markdown
## Deployment

### Docker
```bash
# Build
docker build -t <image-name> .

# Run
docker run -p 3000:3000 --env-file .env <image-name>
```

### Docker Compose
```bash
docker compose up -d
```

### Production Checklist
- [ ] Set `NODE_ENV=production` or equivalent
- [ ] Configure database connection string
- [ ] Set up SSL/TLS certificates
- [ ] Configure logging and monitoring
- [ ] Set up backup strategy for persistent data
```

---

### 5. Health Checks & Monitoring

If the app exposes health endpoints (check source or config):

```markdown
### Health Checks

| Endpoint             | Expected Response               |
| -------------------- | ------------------------------- |
| `/health`            | `{"status": "ok"}`              |
| `/health/ready`      | `{"status": "ok"}`              |
| `/metrics`           | Prometheus metrics format        |
```

---

## Generating the Setup Script

If the project has NO existing setup script AND the user asked for automation,
generate `scripts/setup.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Setting up <project-name> ==="

# Prerequisites check
command -v <lang> >/dev/null 2>&1 || { echo "Error: <lang> is required"; exit 1; }

# Clone if needed
if [ ! -d "<dirname>" ]; then
    git clone <repo-url>
    cd <dirname>
else
    cd <dirname>
    git pull
fi

# Install dependencies
<package-manager> install

# Configuration
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from template — please edit with your values"
fi

echo "=== Setup complete ==="
echo "Run: <start-command>"
```

Also generate a minimal `scripts/dev.sh` for starting the dev environment:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Start development environment
echo "Starting development environment..."

# Start dependencies (Docker Compose for services)
if [ -f "docker-compose.yml" ]; then
    docker compose up -d db cache
fi

# Start the app in dev mode
<dev-command>
```

---

## Common Pitfalls

| Pitfall                            | Detection                                     | Fix                                              |
| ---------------------------------- | --------------------------------------------- | ------------------------------------------------ |
| Missing env var defaults           | Skill says "set X" without documented default  | Check .env.example for values, or source for defaults |
| Hard-coded secret values           | Password/token in generated scripts            | Always use placeholder values: `your-api-key-here` |
| Outdated Docker setup              | Compose file references old image versions     | Document the current compose; note version check |
| Missing platform-specific notes    | Script assumes macOS/Linux only                | Add Windows notes (PowerShell alternatives)      |
| Overlooking dev/prod differences   | Script uses production flags in dev            | Separate dev scripts from prod configs           |
| Ignoring health check endpoints    | No monitoring info in ops docs                 | Search source for `/health`, `/ready`, `/metrics`|
| Not checking for existing scripts  | Duplicating the project's own setup.sh         | Check for existing scripts before generating     |
