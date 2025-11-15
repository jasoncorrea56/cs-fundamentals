# MAKEFILE - Targets & Usage

This document explains the **Makefile** targets provided for local k8s/dev workflows and checks.

---

## 1. Environment Variables

- `MINIKUBE_PROFILE` - Minikube profile name (default: `minikube`)
- `DEV_NS` - dev namespace (default: `csf-dev`)
- `DEV_RELEASE` - Helm release name (default: `csf`)
- `DEV_ENV_PRIMARY` - dev overlay secret env file (default: `deploy/k8s/overlays/dev/.local.secret.env`)

---

## 2. Cluster & Dev Env

- `k8s-up` - Start Minikube with tuned resources and DNS settings.
- `k8s-env` - Configure the current shell’s Docker environment to point at Minikube’s Docker daemon.
- `dev-namespace` - Create or ensure the dev namespace (`csf-dev`) exists.

---

## 3. Images & Secrets

- `dev-image` - Build the `cs-fundamentals:dev` Docker image **inside Minikube’s Docker daemon**, so pulls from k8s succeed:

  ```bash
  eval "$(minikube docker-env)" && docker build -t cs-fundamentals:dev .
  ```

- `dev-secrets` - Strictly ensures the dev secret file exists and applies secrets via Kustomize:

  - Fails fast if `DEV_ENV_PRIMARY` is missing.
  - Uses `kustomize build deploy/k8s/overlays/dev` or `kubectl kustomize` as a fallback.
  - Pipes the rendered manifests into `kubectl apply -f -`.

---

## 4. Helm Install (Dev)

- `dev-install` - Build image and secrets, then install/upgrade the Helm release into `csf-dev`:

  ```bash
  helm upgrade --install csf ./helm     -f helm/values-minikube.yaml     -n csf-dev --create-namespace --wait --timeout 5m
  ```

- `init` - Friendly orchestrator that:
  1. Starts Minikube (`k8s-up`)
  2. Creates dev namespace (`dev-namespace`)
  3. Sets up dev secrets (`dev-secrets`)
  4. Builds dev image (`dev-image`)

  This is the recommended entrypoint for first‑time local k8s setup.

---

## 5. Dev Loop (Skaffold)

- `dev` - Exports `DB_URL` from `.env` and runs Skaffold:

  ```bash
  export DB_URL="$(grep -E '^DB_URL=' .env | cut -d= -f2-)"
  skaffold dev -p minikube
  ```

- `dev-in-node` - Similar to `dev` but explicitly configures Docker env to Minikube:

  ```bash
  eval "$(minikube -p minikube docker-env)" && skaffold dev -p minikube
  ```

- `down` - Deletes Skaffold‑managed resources:

  ```bash
  skaffold delete -p minikube || true
  ```

- `k8s-down` - Deletes the entire Minikube cluster/profile:

  ```bash
  minikube delete -p minikube
  ```

These are documented end‑to‑end in [LOCAL-K8S.md](LOCAL-K8S.md).

---

## 6. Quality & Tests

- `lint` - Runs:
  - `mypy --show-error-codes --pretty .`
  - `ruff check .`
  - `ruff format .`

- `semgrep` - Runs Semgrep and emits a JSON summary piped through `jq`.

- `semgrep-deep` - Runs Semgrep with SARIF output for deeper integration.

- `tests` - Runs `pytest -q`.

These are referenced in [DEVELOPER.md](DEVELOPER.md) and [SECURITY.md](SECURITY.md).

---

## 7. Verification

- `verify` - Operator‑centric target that validates a running deployment in namespace `csf`.

Steps:

1. List deployments/RS/pods.
2. Show deployment conditions for `csf-cs-fundamentals`.
3. Probe `/api/v1/healthz` (if the service exists).
4. Check env vars contain critical values (`DB_URL`, `TMPDIR`).
5. Ensure `/tmp` is writable in the pod.
6. Lint the Helm chart and preview rendered manifests.

This is documented in more detail in [OPERATIONS.md](OPERATIONS.md) and [EKS.md](EKS.md).

---

In short:

- **Use `make init` + `make dev`** for local k8s dev.
- **Use `make lint` + `make tests`** before committing.
- **Use `make verify`** after a deploy to ensure everything is wired correctly.
