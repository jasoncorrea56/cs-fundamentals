# TECH - Architecture & Design

This document explains the **technical shape** of cs-fundamentals: how it’s wired and why.

---

## 1. Application Shape

- **Python 3.11+** service using **FastAPI (0.115+)**
- Core domain:
  - Data structures (graphs, trees, stacks, queues, etc.)
  - Algorithms and patterns (DFS, BFS, sliding window, etc.)
  - Practice vs. reference implementations, validated with pytest
- Exposed via **FastAPI endpoints**:
  - Health + diagnostics (`/api/v1/healthz`, `/configz`, `/version`)
  - Practice exploration (`/api/v1/targets`, additional practice endpoints)

Configuration is loaded via **`pydantic-settings`** from environment variables, keeping builds immutable and config external.

---

## 2. Process & Concurrency Model

The service follows a **12‑factor style process model**:

- **In‑container concurrency**:
  - Controlled via `WEB_CONCURRENCY` (number of worker processes).
- **Horizontal scaling**:
  - Multiple containers/pods behind a load balancer.
  - Service instances are stateless; configuration comes from env and external services.

Runtime knobs:

- Scale workers per container:

  ```bash
  WEB_CONCURRENCY=4 docker compose --profile prod up --build
  ```

- Override listening port:

  ```bash
  PORT=9000 docker compose --profile prod up --build
  ```

---

## 3. Configuration & Environment

- The app reads configuration from `.env` (and other env sources).
- Docker Compose and Kubernetes load env vars into the container.
- `cs_fundamentals.config.Settings` encapsulates runtime configuration, including:
  - DB URL
  - Logging config
  - Environment name
  - Other service toggles

For local bootstrap:

```bash
cp local.env .env
cp local.secret.env deploy/k8s/overlays/dev/.local.secret.env
```

---

## 4. Logging

Application logs are **structured event streams**, not ad‑hoc prints:

- Each request gets a unique `X-Request-ID` (propagated or generated).
- All log lines for a request include this ID for tracing in log aggregation.

Key logging env vars:

- `LOG_LEVEL` (minimum log level)
  - `DEBUG`, `INFO`, `WARNING`, `ERROR`
- `LOG_FORMAT` (output format)
  - `json`, `console`

Examples:

- Human‑readable logs during development:

  ```bash
  LOG_FORMAT=console LOG_LEVEL=DEBUG docker compose --profile dev up
  ```

- Structured JSON logs for production:

  ```bash
  LOG_FORMAT=json LOG_LEVEL=INFO docker compose --profile prod up
  ```

---

## 5. Admin / One‑Off Processes

Admin processes run in the same containerized environment:

```bash
docker compose run --rm admin <command>
docker compose run --rm admin health
```

This keeps “management tasks” and the main app using the same dependencies and environment.

---

## 6. Procfile

A `Procfile` at the project root defines the web process entrypoint:

- Supports platforms like **Heroku, Dokku, Render, Railway**.
- Encodes a single, authoritative process definition for the web service.
- Lets supported platforms auto‑detect and scale the web process without bespoke config.

---

## 7. Tooling Overview

Key tools and how they fit:

- **uv** - dependency & venv management; reproducible Python envs.
- **pytest** - tests and coverage.
- **ruff** - linting and formatting.
- **mypy** - static typing, enforced via CI.
- **MonkeyType** - runtime‑driven type inference to accelerate type coverage.
- **Semgrep** - application security scanning (SAST).
- **Trivy** - filesystem and container image vulnerability scanning; secrets scanning.
- **OSV scanner** - dependency vulnerability checks.
- **Syft** - SBOM generation for transparency and supply chain auditing.

See [DEVELOPER.md](DEVELOPER.md) and [SECURITY.md](SECURITY.md) for commands.

---

## 8. Containers & Orchestration (High Level)

- Dockerfile builds a **versioned, immutable image** (tagged with app version + Git SHA).
- Docker Compose profiles:
  - `dev`: hot reload, mounted source.
  - `prod`: immutable runtime image.
- Kubernetes:
  - Helm chart encapsulates k8s manifests.
  - Skaffold dev profile drives the local inner loop.
  - EKS + ALB Ingress + AWS Secrets Manager in production.

For full k8s details see [KUBERNETES.md](KUBERNETES.md) and [EKS.md](EKS.md).

---

## 9. CI/CD Overview

- GitHub Actions pipelines run:
  - Lint + type checks
  - Pytest
  - Security scanning (Semgrep, Trivy, OSV)
  - SBOM generation
  - Docker build and push to registry
- Deploy pipelines:
  - Helm‑driven deploy to EKS.
  - Blue/green and canary strategies baked into CD.

For full details, see [CI_CD.md](CI_CD.md).
