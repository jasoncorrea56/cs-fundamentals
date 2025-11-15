# SECURITY - Scanning, Secrets & Hardening

This document covers **application security tooling**, **vulnerability scanning**, and how secrets are handled.

---

## 1. Static Analysis & Vulnerability Scanning

Several tools are integrated into the project and CI.

### 1.1 OSV Scanner

Used for dependency vulnerability scanning via GitHub Actions:

- Docs: <https://google.github.io/osv-scanner/github-action/>

### 1.2 Semgrep

Semgrep is used for static application security testing (SAST):

- Docs: <https://semgrep.dev/docs/>

JSON output:

```bash
uv run semgrep ci \
--verbose \
--config p/ci \
--config p/security-audit \
--config p/python --json \
| jq '.results[] | {check_id, path, start: .start.line, message}'
```

SARIF output (for GitHub Security Code Scanning):

```bash
uv run semgrep ci \
--verbose \
--config p/ci \
--config p/security-audit \
--config p/python --sarif
```

Make targets:

```bash
make semgrep          # JSON summary
make semgrep-strict   # SARIF, deeper scan
```

### 1.3 Trivy

Trivy is used for filesystem and container image scanning.

Docs: <https://trivy.dev/latest/>

Install:

```bash
brew install trivy
```

Or run via Docker:

```bash
docker run --rm -v $(pwd):/app -w /app aquasec/trivy:latest fs .
```

File system scan (secrets):

```bash
trivy fs --scanners secret --format table .
```

Image build & scan:

```bash
docker build -t cs-fundamentals:dev .

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

### 1.4 SBOM (Syft)

The project uses **Syft** for SBOM generation (see badge in main README):

```bash
syft cs-fundamentals:dev -o json > sbom.json
```

SBOMs can be uploaded as CI artifacts or shared with consumers for supply chain transparency.

---

## 2. Secrets Management

### 2.1 Local / Dev

- Local config is stored in:
  - `.env` (based on `local.env`)
  - `deploy/k8s/overlays/dev/.local.secret.env` for K8s dev secrets
- Dev K8s secrets:
  - Created declaratively via Kustomize (or `kubectl kustomize`) and applied via `kubectl`.

Makefile target:

```bash
make dev-secrets
```

Which:

- Validates that `deploy/k8s/overlays/dev/.local.secret.env` exists.
- Uses Kustomize to build and apply the dev overlay.

### 2.2 Production (EKS)

See [EKS.md](EKS.md) for full details.

Highlights:

- Sensitive values (e.g., DB URL) stored in **AWS Secrets Manager**.
- Pods consume secrets via **Secrets Store CSI Driver**.
- An **IRSA** role allows only the app’s ServiceAccount to read the required secret.
- Secrets are synchronized into a namespaced K8s Secret (`csf-db`) with key `DB_URL`.

---

## 3. Logging & Privacy

- Logs are structured JSON (in prod) or console‑friendly (in dev).
- Each request gets a `X-Request-ID` for correlation.
- Avoid logging:
  - Credentials
  - Full tokens
  - Sensitive PII

Operational logging guidance is in [OPERATIONS.md](OPERATIONS.md).

---

## 4. Hardening Practices

- 12‑factor app design: config in env, immutable builds.
- Least privilege IAM via IRSA for k8s workloads.
- Strict separation of:
  - Local/dev secrets
  - Prod secrets (AWS SM + CSI)
- Regular scanning:
  - Dependencies (OSV)
  - Source (Semgrep)
  - Images/filesystem (Trivy)
  - SBOM (Syft)
