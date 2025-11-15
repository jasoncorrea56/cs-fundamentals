# OPERATIONS - Runtime, Logs & Verification

This document is aimed at people **operating** cs-fundamentals in k8s/EKS or Docker.

---

## 1. Runtime Knobs

### 1.1 Concurrency

The service scales via:

- **In‑container concurrency**:
  - `WEB_CONCURRENCY` controls the number of worker processes.
- **Horizontal concurrency**:
  - Multiple pods/containers behind a load balancer.

Example:

```bash
WEB_CONCURRENCY=4 docker compose --profile prod up --build
```

### 1.2 Port

Override the port if needed:

```bash
PORT=9000 docker compose --profile prod up --build
```

---

## 2. Logging

Key env vars:

- `LOG_LEVEL`:
  - `DEBUG`, `INFO`, `WARNING`, `ERROR`
- `LOG_FORMAT`:
  - `json`, `console`

Examples:

- Dev (human‑readable):

  ```bash
  LOG_FORMAT=console LOG_LEVEL=DEBUG docker compose --profile dev up
  ```

- Prod‑style (structured JSON):

  ```bash
  LOG_FORMAT=json LOG_LEVEL=INFO docker compose --profile prod up
  ```

Logging design:

- Structured logs with a per‑request `X-Request-ID`.
- Suitable for ingestion into log aggregation (CloudWatch, ELK, etc.).

---

## 3. Admin / One‑Off Jobs

Run one‑off tasks in the same containerized environment:

```bash
docker compose run --rm admin <command>
docker compose run --rm admin health
```

These share the same image and dependencies as the main web service.

---

## 4. Health & Diagnostics

Core diagnostic endpoints:

- `GET /api/v1/healthz` - health check
- `GET /api/v1/configz` - config snapshot
- `GET /api/v1/version` - version and build info

See [API.md](API.md) for `curl` examples.

---

## 5. Kubernetes / EKS Verification

The `verify` Makefile target encapsulates a set of operational checks against the `csf` namespace:

```bash
make verify
```

It performs:

1. **Deployment & Pod Status**

   ```bash
   kubectl -n csf get deploy,rs,pods
   ```

2. **Deployment Conditions**

   ```bash
   kubectl -n csf describe deploy csf-cs-fundamentals | grep -A5 "Conditions" || true
   ```

3. **Health Endpoint Check**

   Only if the service exists:

   ```bash
   if kubectl -n csf get svc csf-cs-fundamentals >/dev/null 2>&1; then
     curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8080/api/v1/healthz || true
   fi
   ```

4. **Environment Variables**

   Confirms that critical env vars (including secrets) are present:

   ```bash
   kubectl -n csf exec -it deploy/csf-cs-fundamentals -- printenv | grep -E 'DB_URL|TMPDIR' || true
   ```

5. **Writable `/tmp`**

   Ensures the filesystem is writable where expected:

   ```bash
   kubectl -n csf exec -it deploy/csf-cs-fundamentals -- sh -c 'touch /tmp/testfile && ls -l /tmp/testfile' || true
   ```

6. **Helm Lint & Manifest Check**

   ```bash
   helm lint ./helm
   helm get manifest csf -n csf | head -n 30 || true
   ```

This target is particularly useful after a new deploy to confirm:

- Pods are up
- Probes and health endpoints work
- Secrets (`DB_URL`) are correctly wired
- Filesystem permissions are acceptable
- Helm chart is syntactically sane

---

## 6. Local vs. Prod Differences

- **Local Docker Compose**:
  - No AWS integrations by default.
  - Secrets come from `/deploy/k8s/overlays/dev/.local.secret.env` or Compose env files.
- **Local k8s (Minikube)**:
  - Uses K8s Secrets created from local env files.
  - No IRSA or Secrets Manager; everything is purely in‑cluster.
- **Prod EKS**:
  - Uses AWS Secrets Manager + CSI and IRSA.
  - ALB Ingress, ACM certs, and Terraform‑managed configuration.
  - Blue/green and canary deployment strategies.

See [EKS.md](EKS.md) for AWS details and [KUBERNETES.md](KUBERNETES.md) for more k8s commands.

---

## 7. Incident Triage Checklist

When something looks wrong in prod:

1. **Check deployment & pods**: `make verify` or the underlying kubectl commands.
2. **Hit health/version endpoints**: confirm the app is up and at the expected version.
3. **Inspect logs**:
   - Look for high‑frequency errors.
   - Use `X-Request-ID` to trace problem requests.
4. **Validate secrets**:
   - Ensure `DB_URL` and other critical vars show up in `printenv`.
   - Confirm AWS SM/CSI/IAM paths if secrets are missing.
5. **Roll back or re‑deploy**:
   - Use blue/green or canary controls in CI (see [CI_CD.md](CI_CD.md)).
