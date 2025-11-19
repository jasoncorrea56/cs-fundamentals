# EKS - Production Infrastructure & Secrets

This document covers how **cs-fundamentals** runs on **AWS EKS**, including secrets, IRSA, and Ingress.

---

## 1. High‑Level Pieces

On EKS, the service is backed by:

- An EKS cluster (Terraform‑managed)
- AWS ECR registry for container images
- AWS ALB Ingress Controller for HTTP routing + TLS
- AWS Secrets Manager for sensitive config values
- Secrets Store CSI Driver for mounting secrets into pods
- IAM Roles for Service Accounts (IRSA) for least‑privilege access
- Terraform modules to wire it all together (including the Helm app chart)

---

## 2. Secrets via AWS Secrets Manager + CSI

Production uses **AWS Secrets Manager** with the **Secrets Store CSI Driver**.

Terraform provides:

- A JSON secret at path:

  ```text
  csf/db-url
  ```

  With contents:

  ```json
  { "db_url": "..." }
  ```

- An **IRSA role** for ServiceAccount `csf-app`.
- A `SecretProviderClass` named `csf-db-spc` that:
  - Reads the secret from AWS SM.
  - Syncs it into a namespaced K8s Secret `csf-db` with key `DB_URL`.

Helm (Prod):

- Does **not** create the ServiceAccount; it reuses the TF‑managed `csf-app`.
- Mounts the CSI volume (read‑only).
- Reads `DB_URL` from the synced K8s Secret `csf-db`.

Minikube/Dev:

- Uses a standard K8s Secret for convenience (wired via `helm/values-minikube.yaml` and Kustomize overlay).
- No AWS SM/CSI in local dev; just pure K8s secrets.

---

## 3. Ingress, Domain & TLS

Production is fronted by an **AWS Application Load Balancer (ALB)**:

- **Domain**: e.g. `csf.jasoncorrea.dev`
- **TLS**: via ACM certificate
- ALB Ingress annotations & hostnames are injected by Terraform + CI (see [CI_CD.md](CI_CD.md)).

Key properties:

- Terraform **`app_chart` module** passes:
  - `var.app_domain = "csf.jasoncorrea.dev"`
  - `var.acm_certificate_arn = module.acm_csf.certificate_arn`
- CI (`deploy.yaml`) wires these into the `helm upgrade` command:
  - `--set ingress.hosts[0].host=csf.jasoncorrea.dev`
  - ALB/ACM annotations for TLS termination.

Helm defaults in `values-prod.yaml` keep:

- `ingress.enabled=true`
- `className=alb`
- No real hostnames or cert ARNs defined.

This separation ensures:

- App chart remains environment‑agnostic.
- Production domain and TLS details live in **Terraform + CI** instead of chart defaults.

---

## 4. Verifying Production Deployment

The `verify` Makefile target is designed to check a running deployment in namespace `csf`:

```bash
make verify
```

Under the hood it:

1. Checks deployment + pods:

   ```bash
   kubectl -n csf get deploy,rs,pods
   ```

2. Inspects deployment conditions:

   ```bash
   kubectl -n csf describe deploy csf-cs-fundamentals | grep -A5 "Conditions" || true
   ```

3. Checks health endpoint via the service:

   ```bash
   if kubectl -n csf get svc csf-cs-fundamentals >/dev/null 2>&1; then
     curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8080/api/v1/healthz || true
   fi
   ```

4. Confirms key environment variables (especially secrets):

   ```bash
   kubectl -n csf exec -it deploy/csf-cs-fundamentals -- printenv | grep -E 'DB_URL|TMPDIR' || true
   ```

5. Ensures `/tmp` is writable:

   ```bash
   kubectl -n csf exec -it deploy/csf-cs-fundamentals -- sh -c 'touch /tmp/testfile && ls -l /tmp/testfile' || true
   ```

6. Lints the Helm chart and inspects manifests:

   ```bash
   helm lint ./helm
   helm get manifest csf -n csf | head -n 30 || true
   ```

See [OPERATIONS.md](OPERATIONS.md) for how to interpret these checks.

---

## 5. CD Strategies on EKS

On EKS, blue/green and canary deployments are executed via:

- Helm releases with separate **“blue”** and **“green”/“canary”** states.
- Weighted traffic configuration at the ALB/Ingress layer (managed by CI logic).

Strategies (detailed in [CI_CD.md](CI_CD.md)):

- **Blue/Green**
  - Green comes up with 0% traffic.
  - Smoke‑tested via in‑cluster curl pod.
  - On success, traffic is flipped 100% to green and old blue is disabled.
- **Canary**
  - Canary comes up alongside stable.
  - Starts at 0% traffic; smoke‑tested.
  - On success, traffic may be shifted gradually (1-99%).
    - Or promotion to 100% where canary becomes new stable.

---

## 6. Observability (Pointer)

EKS observability (Container Insights, CloudWatch, metrics) is set up via Terraform and standard AWS tooling. At the app level:

- Logs are structured with request IDs.
- Env‑driven logging config (`LOG_LEVEL`, `LOG_FORMAT`).
- Health/diagnostic endpoints for fast checks.

See [OPERATIONS.md](OPERATIONS.md) for runtime/logging details and [KUBERNETES.md](KUBERNETES.md) for generic k8s commands.
