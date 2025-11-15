# KUBERNETES - Helm, Skaffold & Manifests

This document covers how **cs-fundamentals** is deployed onto Kubernetes clusters in general
(local or cloud), with EKS‑specific details in [EKS.md](EKS.md).

---

## 1. Helm Chart Basics

The app is packaged as a Helm chart (`./helm`).

### 1.1 Installing the Chart

Basic install with explicit image:

```bash
helm install csf ./cs-fundamentals   --set image.repository=ghcr.io/your-org/cs-fundamentals   --set image.tag=latest
```

### 1.2 With Ingress

Example using nginx ingress:

```bash
helm install csf ./cs-fundamentals   --set ingress.enabled=true   --set ingress.className=nginx   --set ingress.hosts[0].host=csf.localtest.me
```

---

## 2. Local Minikube Values

For local k8s development, `helm/values-minikube.yaml` is used:

```bash
helm upgrade --install csf ./helm   -f helm/values-minikube.yaml   -n csf-dev --create-namespace
```

Secrets in Minikube/dev are represented as a plain K8s Secret (for convenience). See [LOCAL-K8S.md](LOCAL-K8S.md) for how these get applied.

---

## 3. Production Values (High Level)

Production uses `helm/values-prod.yaml` plus overrides from CI/Terraform:

```bash
helm upgrade --install csf ./helm   -f helm/values-prod.yaml   -n csf
```

However, **Ingress hosts and TLS** are not hard‑coded in the chart; they are injected dynamically by:

- Terraform (via an app_chart module)
- CI (GitHub Actions `deploy.yaml`)
- Environment‑specific Helm value overrides

See [EKS.md](EKS.md) and [CI_CD.md](CI_CD.md) for the full story.

---

## 4. Skaffold Dev Loop

Skaffold is used to manage the local Kubernetes development loop:

```bash
skaffold dev -p minikube -v info
```

Behavior:

- Watches source files for changes.
- Rebuilds images using Minikube’s Docker daemon.
- Applies updated manifests via Helm/Kustomize.
- Streams logs and events.

This is wrapped by `make dev` (see [LOCAL-K8S.md](LOCAL-K8S.md) and [MAKEFILE.md](MAKEFILE.md)).

---

## 5. Dev Namespace & Secrets

The dev namespace and secrets are created declaratively:

- Namespace: `csf-dev`
- Secret config sourced from `deploy/k8s/overlays/dev/.local.secret.env`

Command path (from the Makefile):

```bash
# Create/ensure namespace
kubectl create namespace csf-dev --dry-run=client -o yaml | kubectl apply -f -

# Build and apply dev overlay (prefers kustomize if installed)
if command -v kustomize >/dev/null 2>&1; then
  kustomize build deploy/k8s/overlays/dev
else
  kubectl kustomize deploy/k8s/overlays/dev
fi | kubectl apply -f -
```

For a full dev bootstrap on Minikube, see [LOCAL-K8S.md](LOCAL-K8S.md) (`make init`, `make dev`, etc.).

---

## 6. Verification (Cluster Perspective)

Once deployed (local or prod), you can verify the app deployment and resources:

```bash
kubectl -n csf get deploy,rs,pods
```

Inspect deployment conditions:

```bash
kubectl -n csf describe deploy csf-cs-fundamentals | grep -A5 "Conditions" || true
```

Check the service:

```bash
kubectl -n csf get svc csf-cs-fundamentals
```

If the service exists and is reachable, the verify script (see [OPERATIONS.md](OPERATIONS.md)) will also probe `/api/v1/healthz`.

---

## 7. Where EKS Comes In

On EKS, additional pieces are layered on top:

- AWS ALB Ingress Controller
- AWS Secrets Manager (via Secrets Store CSI Driver)
- IRSA for app pods
- Terraform modules for cluster and app chart

Those are described in [EKS.md](EKS.md).
