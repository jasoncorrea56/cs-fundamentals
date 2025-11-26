# LOCAL-K8S - Minikube + Skaffold Workflow

This document explains how to run **cs-fundamentals** on a local Kubernetes cluster using **Minikube** and **Skaffold**.

It builds directly on the Makefile targets described in [MAKEFILE.md](MAKEFILE.md).

---

## 1. Prerequisites

- **Minikube**
- **kubectl**
- **Skaffold**
- **Docker**
- Optional: `kustomize` (otherwise `kubectl kustomize` will be used)

Also ensure you have the local env files:

```bash
cp local.env .env
cp local.secret.env deploy/k8s/overlays/dev/.local.secret.env
```

`deploy/k8s/overlays/dev/.local.secret.env` must at least contain `DB_URL=...`.

---

## 2. One‑Time-ish Initialization

Run:

```bash
kubectl config use-context minikube
make init
```

This will:

1. **Start Minikube** with tuned resources and DNS:

   ```bash
   minikube start -p minikube --cpus=4 --memory=6g      --dns-proxy=true      --driver=docker      --docker-opt=dns=8.8.8.8      --docker-opt=dns=1.1.1.1
   ```

2. **Create dev namespace** `csf-dev`:

   ```bash
   kubectl create namespace csf-dev --dry-run=client -o yaml | kubectl apply -f -
   ```

3. **Create dev secrets** from the overlay env file:

   ```bash
   # fails if deploy/k8s/overlays/dev/.local.secret.env is missing
   if command -v kustomize >/dev/null 2>&1; then
     kustomize build deploy/k8s/overlays/dev
   else
     kubectl kustomize deploy/k8s/overlays/dev
   fi | kubectl apply -f -
   ```

4. **Build dev image** inside Minikube’s Docker daemon:

   ```bash
   eval "$(minikube docker-env)" && docker build -t cs-fundamentals:dev .
   ```

When `make init` finishes, you have:

- A running Minikube cluster.
- Dev namespace `csf-dev`.
- Dev secrets configured.
- A local dev image ready to be used by Skaffold/Helm.

---

## 3. Dev Loop with Skaffold

To start the continuous dev loop:

```bash
make dev
```

This:

- Extracts `DB_URL` from `.env`:

  ```bash
  export DB_URL="$(grep -E '^DB_URL=' .env | cut -d= -f2-)"
  ```

- Runs Skaffold:

  ```bash
  skaffold dev -p minikube
  ```

Skaffold will:

- Watch source files.
- Rebuild the image (using Minikube’s Docker daemon).
- Apply updated manifests (Helm/Kustomize).
- Stream logs and status.

If you want to make sure the Docker env is explicitly pointing at Minikube, you can use:

```bash
make dev-in-node
```

Which runs:

```bash
eval "$(minikube -p minikube docker-env)" && skaffold dev -p minikube
```

---

## 4. Inspecting the Dev Deployment

Once Skaffold has deployed:

```bash
kubectl -n csf-dev get deploy,rs,pods,svc
helm -n csf-dev status csf --show-resources
```

You can also port‑forward or use Minikube ingress as configured to hit the API.

---

## 5. Tearing Down

To remove Skaffold‑managed resources (but keep the cluster):

```bash
make down
# under the hood: skaffold delete -p minikube || true
```

To delete the entire Minikube cluster:

```bash
make k8s-down
# under the hood: minikube delete -p minikube
```

---

## 6. When to Use Local k8s vs. Docker Compose

- Use **Docker Compose** when:
  - You just want to validate the app logic.
  - You’re not touching k8s‑specific behavior.
- Use **Minikube + Skaffold** when:
  - You’re working on Helm templates, Secrets, or K8s config.
  - You want to emulate the EKS deployment more closely.
  - You need to debug IRSA/Secrets/Ingress behavior (locally approximated).

See:

- [RUNBOOK.md](RUNBOOK.md) for high‑level “run & curl” instructions.
- [KUBERNETES.md](KUBERNETES.md) for generic k8s operations.
- [EKS.md](EKS.md) for the production EKS details.
