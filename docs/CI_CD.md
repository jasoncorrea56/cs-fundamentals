# CI/CD – Build, Scan & Deploy Pipelines

This document explains how **cs-fundamentals** is built, scanned, and deployed across **three environments**:

- **Dev** – branch pushes
- **QA** – merges to `main`
- **Prod** – manual, explicit promotion only

The design goals:

- One workflow per event (no duplicate runs)
- Immutable, scanned images
- Environment-aware, GitHub Environments–backed deploys
- Manual-only production promotion

---

## 1. Build / Release / Run Model

The project follows a **three-stage** model:

1. **Build**
   - The `Dockerfile` produces a **versioned, immutable image**.
   - Images are tagged with app version + Git SHA (e.g. `0.7.6-a71e692`).
2. **Release**
   - A release is a specific image + a set of environment configuration
     (Helm values, Kubernetes manifests).
3. **Run**
   - Containers run the image with environment-appropriate configuration:
     - Local Docker / `docker compose`
     - EKS workloads via Helm

Automated builds are validated by the CI/CD workflows described below, which:

- Run linting and static checks
- Run `pytest` with coverage
- Run security scanners (OSV, Semgrep, Trivy, Syft SBOM)
- Build and publish images to GHCR/ECR
- Deploy to EKS based on branch + environment rules

---

## 2. CI Tools & Static Analysis

Static analysis and security tooling is shared across PR CI and push-based CD.

### 2.1 OSV

GitHub Action integration:

- <https://google.github.io/osv-scanner/github-action/>

Used to detect known vulnerabilities in dependencies by scanning a requirements manifest exported from `uv.lock`.

### 2.2 Semgrep

Application security platform for code scanning:

- <https://semgrep.dev/docs/>

Example local runs:

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
docker run --rm -v "$(pwd)":/app -w /app aquasec/trivy:latest fs .
```

File system scan (vulns/secrets/licenses):

```bash
trivy fs   --scanners vuln,secret,license   --format table   ./
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

The project tracks SBOM generation via **Syft**.

Example local SBOM command:

```bash
syft cs-fundamentals:dev -o json > sbom.json
```

CI also generates a CycloneDX SBOM and uploads it as an artifact.

---

## 3. GitHub Actions Architecture (3 Environments)

The CI/CD system is split into three main workflows:

| Workflow Name                        | File                                  | Triggers                  | Responsibility                              |
|-------------------------------------|----------------------------------------|---------------------------|--------------------------------------------|
| **Automation – Lint/Scan/Test**     | `.github/workflows/automation.yaml`    | `pull_request -> main`   | PR CI only (lint, tests, scans). No deploy. |
| **CD – Build & Deploy (Dev/QA)**    | `.github/workflows/build-and-deploy.yaml` | `push` (any branch)   | Build, scan, push, then deploy to Dev or QA. |
| **CD – Manual Deploy to EKS**       | `.github/workflows/manual-deploy.yaml` | `workflow_dispatch`      | Deploy an existing image tag to Dev/QA/Prod. |

### 3.1 Event Routing (One Workflow Per Event)

- **Pull Requests → CI only**
  - `automation.yaml` runs on PRs targeting `main`.
  - Lint / tests / scans only.
  - No images are built or pushed, and no deployment occurs.

- **Pushes → Build & Deploy**
  - `build-and-deploy.yaml` runs on **any branch push**.
  - Always builds, scans, and pushes a new image.
  - Deploy target is inferred from the branch:
    - `main` → **QA**
    - any other branch → **Dev**

- **Manual Promotion → Deploy only**
  - `manual-deploy.yaml` runs **only** when invoked from the UI.
  - Deploys an existing image tag to **Dev**, **QA**, or **Prod**.
  - No build or scan is performed in this workflow.

This design enforces:

- PRs run fast, safe CI without touching infra.
- Every push has a reproducible, immutable image.
- Dev and QA receive continuous updates from branches / main.
- Prod is fully manual and deliberate.

---

## 4. Secrets & GitHub Environments

CD workflows rely on a combination of **repository-level** secrets and **environment-level** secrets.

### 4.1 Repository Secrets (Shared by All Envs)

Set once at:

> **Settings → Secrets and variables → Actions → Repository secrets**

| Secret              | Description                                           |
|---------------------|-------------------------------------------------------|
| `AWS_ROLE_TO_ASSUME` | IAM role GitHub OIDC assumes for deployments        |
| `AWS_REGION`        | Region for EKS/ECR (e.g. `us-west-2`)                |
| `ECR_REGISTRY`      | ECR account/registry (e.g. `XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com`) |

These are reused by all environments (Dev/QA/Prod). If you ever move Prod to a different AWS account, you can override these at the environment level.

### 4.2 Environment Secrets (Environment-Specific)

Set at:

> **Settings → Environments → (dev / qa / prod)**

#### `dev` environment

| Secret             | Value                  |
|--------------------|------------------------|
| `EKS_CLUSTER_NAME` | `csf-dev-cluster`      |

#### `qa` environment

| Secret             | Value                  |
|--------------------|------------------------|
| `EKS_CLUSTER_NAME` | `csf-qa-cluster`       |

#### `prod` environment

| Secret             | Value                         |
|--------------------|-------------------------------|
| `EKS_CLUSTER_NAME` | `csf-prod-cluster`            |
| `APP_DOMAIN`       | e.g. `csf-prod.jasoncorrea.dev` |
| `ACM_CERT_ARN`     | ACM cert ARN for prod ingress |

Secrets precedence:

> environment secret → repo secret → org secret

So you only need to override what truly differs per environment.

---

## 5. Environment Mapping & CD Behavior

### 5.1 Dev / QA (Automatic)

- **Push to non-main branches**
  - `build-and-deploy.yaml` builds, scans, pushes image.
  - CD deploys to **Dev** (`deploy_env=dev`, GitHub Environment: `dev`).
  - Use this for feature branches and PR heads.

- **Push to main**
  - Usually happens on **PR merge**.
  - `build-and-deploy.yaml` builds, scans, pushes image.
  - CD deploys to **QA** (`deploy_env=qa`, GitHub Environment: `qa`).
  - QA always runs the latest `main` build.

### 5.2 Prod (Manual Only)

- No automatic deploys to Prod from pushes or PRs.
- Use **“CD – Manual Deploy to EKS”** workflow from the Actions UI:
  - Select environment (`dev`, `qa`, or `prod`).
  - Select an existing ECR image tag.
  - Optionally configure canary behavior.
- This ensures Prod promotion is explicit and auditable.

---

## 6. Helm, Terraform & Ingress Host Overrides

Ingress host configuration for **production** is **not** statically defined in Helm.
Instead, it is dynamically injected during deployment:

| Layer               | Source                | Responsibility |
|---------------------|-----------------------|----------------|
| **Terraform**       | `infra/modules/app_chart` + env roots | Passes `var.app_domain` and ACM cert ARN into the Helm release. Ensures Ingress points to the correct domain and certificate. |
| **CI/CD (GitHub)**  | `deploy.yaml`         | During `helm upgrade`, overrides Ingress host and annotations for the current environment (especially `DEPLOY_ENV=prod`). |
| **Helm defaults**   | `helm/values-*.yaml` | Baseline chart config (dev/qa/prod overlays). Host values can be placeholders; actual prod routing is controlled by TF + CI. |

> 🔒 **Security:** Production host and TLS configuration are **authoritative** from infra and CI, not local values files. Developers can deploy locally without touching real DNS or ACM certs.

#### 6.1 Value Injection Flow (Local → CI → Terraform)

| Layer                     | Source of Truth           | Purpose                                   | Example Override |
|---------------------------|---------------------------|-------------------------------------------|------------------|
| **Helm (values-prod.yaml)** | `helm/values-prod.yaml` | Baseline chart config for local/test.     | `ingress.enabled=true`, `className=alb` |
| **CI/CD (GitHub Actions)**  | `.github/workflows/deploy.yaml` | Overrides hosts/annotations per env. | `--set ingress.hosts[0].host=${APP_DOMAIN}` |
| **Terraform (app_chart)**   | `infra/envs/*/main.tf`  | Authoritative domain & ACM wiring.        | `var.app_domain`, `var.acm_certificate_arn` |

---

## 7. Deployment Strategies (Blue/Green & Canary)

The CD pipeline supports:

- **Blue/Green**: full cutover once “green” is healthy.
- **Canary**: percentage-based rollout with weights.

These are configured primarily via **Prod** deploys, but the same logic can be used for other environments if desired.

### 7.1 Blue/Green Flow

1. Stage **green** deployment.
2. Set green traffic weight to `0%`.
3. Smoke test green (via in-cluster curl pod).
   - If **fail**: disable green.
   - If **pass**:
     - Promote green weight to `100%`.
     - Disable old stable blue.

### 7.2 Canary Flow

1. Stage **canary** deployment (stable remains pinned).
2. Set canary traffic weight to `0%`.
3. Smoke test canary (in-cluster curl).
   - If **fail**: disable canary.
   - If **pass**:
     - Shift traffic `(1–99%)` to canary, or
     - Promote to `100%` and treat former canary as new stable.

Traffic shifting is managed at the ingress/load-balancer layer (ALB in production EKS).

---

## 8. Manual Deployment (UI Trigger)

The **“CD – Manual Deploy to EKS”** workflow supports **manual triggers** via the GitHub Actions UI, without requiring a new commit.

### 8.1 Workflow Inputs

- `deploy_env`: target environment (`dev`, `qa`, or `prod`)
- `image_tag`: ECR image tag to deploy (`0.7.6-a71e692`, `latest`, etc.)
- `canary_enabled`: enables/disables canary path (`true` / `false`)
- `canary_weight`: canary traffic weight `0–100`
  - `0` = stage-only
  - `100` = promote to stable
- `force_prod`: advanced flag; normally left `false`

### 8.2 Steps to Trigger a Manual Deploy

1. Navigate to **Actions → CD – Manual Deploy to EKS**.
2. Click **“Run workflow”**.
3. Choose:
   - `deploy_env`: `dev`, `qa`, or `prod`
   - `image_tag`: an existing image tag in ECR
   - `canary_enabled`: `false` for a straight deploy, `true` for staged/canary
   - `canary_weight`: `0` to stage only, or a higher weight for rollout
4. Click **Run**.

The workflow will:

- Prepare a minimal `image-refs.env` compatible with `deploy.yaml`.
- Perform `helm upgrade` with environment-specific overrides.
- Deploy either stable or staged canary.
- Apply ingress settings (domain, annotations) as appropriate for the target env.

> ⚠️ **Branch requirement:** Manual deploys use the workflow definition from the branch they are run against. When testing CD changes, trigger runs on your feature branch.

---

## 9. Local CI-Like Checks

To approximate what CI does locally:

```bash
make lint            # mypy + ruff check + ruff format
make tests           # pytest
make semgrep         # JSON summary
make semgrep-strict  # SARIF for deeper runs
# Trivy / Syft as described above
```

This is a good pre-push / pre-PR routine.

---

## 10. Summary

- **PRs** validate code quality and security, but do not deploy.
- **Branch pushes** automatically build, scan, push, and deploy to **Dev**.
- **Merges to main** automatically build, scan, push, and deploy to **QA**.
- **Prod** is updated via a **manual, explicit promotion** using a known image tag.
- All deploys are backed by:
  - Immutable, scanned images
  - Environment-aware secrets and GitHub Environments
  - Terraform-managed infra and TLS
  - Helm-based application rollouts

This architecture keeps CI/CD both **developer-friendly** and **production-safe**, while making every environment rebuildable and auditable end-to-end.
