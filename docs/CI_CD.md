# CI/CD - Build, Scan & Deploy Pipelines

This document explains how cs-fundamentals is built, scanned, and deployed.

---

## 1. Build / Release / Run Model

The project follows a **three‑stage** model:

1. **Build**
   - Dockerfile produces a **versioned, immutable image**.
   - Image is tagged with app version and Git SHA.
2. **Release**
   - Release ties a specific build to a set of environment configuration (`.env`, Helm values).
3. **Run**
   - Containers (local or k8s) execute the image with the provided configuration.
   - `docker compose` profiles:
     - `dev` - hot reload, mounted source
     - `prod` - immutable runtime image

Automated builds are validated by `.github/workflows/build.yaml`, which:

- Runs linting (`ruff`, `mypy`)
- Runs `pytest` with coverage
- Runs static analysis and security scanners
- Builds and publishes images to a registry (GHCR/ECR) on `main` merges

---

## 2. CI Tools & Static Analysis

### 2.1 OSV

GitHub Action integration:

- <https://google.github.io/osv-scanner/github-action/>

Used to detect known vulnerabilities in dependencies.

### 2.2 Semgrep

Application security platform for code scanning:

- <https://semgrep.dev/docs/>

JSON report:

```bash
uv run semgrep ci \
--verbose \
--config p/ci \
--config p/security-audit \
--config p/python --json \
| jq '.results[] | {check_id, path, start: .start.line, message}'
```

SARIF report (for GitHub Security tab):

```bash
uv run semgrep ci \
--verbose \
--config p/ci \
--config p/security-audit \
--config p/python --sarif
```

### 2.3 Trivy

Docs: <https://trivy.dev/latest/>

Install locally (recommended):

```bash
brew install trivy
```

Or run as a container:

```bash
docker run --rm -v $(pwd):/app -w /app aquasec/trivy:latest fs .
```

File system scan (secrets):

```bash
trivy fs --scanners secret --format table .
```

Image build:

```bash
docker build -t cs-fundamentals:dev .
```

Image scan (vulns):

```bash
trivy image \
--format table \
--exit-code 1 \
--ignore-unfixed \
--vuln-type os,library \
--scanners vuln \
--severity CRITICAL,HIGH \
--ignorefile .trivyignore \
cs-fundamentals:dev
```

### 2.4 SBOM (Syft)

The project tracks SBOM generation via **Syft** (badge in main README). A typical local SBOM command (example):

```bash
syft cs-fundamentals:dev -o json > sbom.json
```

---

## 3. Helm, Terraform & Ingress Host Overrides

Ingress host configuration for **production** is **not** statically defined in Helm.

Instead, it is dynamically injected during deployment:

| Layer               | Source              | Responsibility |
|---------------------|---------------------|----------------|
| **Terraform**       | `modules/app_chart` | Passes `var.app_domain` (`csf.example-domain.com`) and ACM certificate ARN directly into the Helm release. Ensures the Ingress always points to the correct domain and certificate. |
| **CI/CD (GitHub)**  | `deploy.yaml`       | During the `helm upgrade` step, overrides Ingress host and annotations for the current environment (`DEPLOY_ENV=prod`). |
| **Helm defaults**   | `helm/values-prod.yaml` | Minimal fallback (`ingress.enabled=true`, `className=alb`) for local or test deployments. Host values are placeholders only. |

> 🔒 **Security:** Production host and TLS configuration are **authoritative** from infra and CI, not local values files. Developers can deploy locally without touching real DNS or ACM certs.

#### Value Injection Flow (Local -> CI -> Terraform)

| Layer                     | Source of Truth         | Purpose                                   | Example Override |
|---------------------------|-------------------------|-------------------------------------------|------------------|
| **Helm (values-prod.yaml)** | `helm/values-prod.yaml` | Baseline chart config for local/test.     | `ingress.enabled=true`, `className=alb` |
| **CI/CD (GitHub Actions)**  | `.github/workflows/deploy.yaml` | Overrides hosts/annotations per env. | `--set ingress.hosts[0].host=csf.example-domain.com` |
| **Terraform (app_chart)**   | `infra/envs/prod/main.tf` | Authoritative domain & ACM wiring.      | `var.app_domain = "csf.example-domain.com"`; `var.acm_certificate_arn = module.acm_csf.certificate_arn` |

---

## 4. Deployment Strategies (Blue/Green & Canary)

The CD pipeline supports:

- **Blue/Green**: full cutover once “green” is healthy.
- **Canary**: percentage‑based rollout with weights.

### 4.1 Blue/Green Flow

1. Stage **green** deployment.
2. Set green traffic weight to `0%`.
3. Smoke test green (via in‑cluster curl pod).
   - If **fail**: disable green.
   - If **pass**:
     - Promote green weight to `100%`.
     - Disable old stable blue.

### 4.2 Canary Flow

1. Stage **canary** deployment (stable remains pinned).
2. Set canary traffic weight to `0%`.
3. Smoke test canary (in‑cluster curl).
   - If **fail**: disable canary.
   - If **pass**:
     - Shift traffic `(1-99%)` to canary, or
     - Promote to `100%` and treat former canary as new stable.

The underlying traffic shifting is managed at the ingress/load‑balancer layer (ALB in production EKS).

---

## 5. Manual Production Deployment (UI Trigger)

The `CD - Deploy to EKS` workflow supports **manual triggers** via the GitHub Actions UI, without needing a new commit.

### 5.1 Workflow Inputs

- `deploy_env`: target environment (`dev` or `prod`)
- `force_prod`: allows UI‑triggered production deploys without main/tags (for single environment testing)
- `canary_enabled`: enables/disables canary path
- `canary_weight`: canary traffic weight `0-100`
- `canary_image_tag`: explicit image tag override

### 5.2 Steps to Trigger a Manual Prod Deploy

1. Navigate to **Actions -> CD -> Deploy to EKS**.
2. Click **Run workflow**.
3. Fill in:
   - `deploy_env`: `prod`
   - `force_prod`: `false`
   - `canary_enabled`: `false` (or `true` for canary testing)
   - `canary_weight`: `0` (or desired percentage)
   - `canary_image_tag`: `<version>`
4. Click **Run**.

The workflow will:

- Resolve the image tag.
- Perform `helm upgrade` with environment‑specific overrides.
- Deploy either stable or staged canary.
- Apply ingress settings (domain, annotations) for prod.

> ⚠️ **Branch requirement:** Manual deploys always use the workflow definition from the branch they are run against. When testing CD changes, make sure you trigger the run on your feature branch.

---

## 6. Local CI‑Like Checks

If you want to approximate what CI does locally:

```bash
make lint            # mypy + ruff check + ruff format
make tests           # pytest
make semgrep         # JSON summary
make semgrep-strict  # SARIF for deeper runs
# Trivy / syft as described above
```

This is a good pre‑push/pre‑PR routine.
