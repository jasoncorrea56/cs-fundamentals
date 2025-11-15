# RUNBOOK - Local Execution & Basic Usage

This runbook is focused on **“how do I run this service locally and hit it?”**
It assumes you are on a developer machine with Docker available.

For deeper dev setup (tooling, tests, type hints), see [DEVELOPER.md](DEVELOPER.md).
For Minikube/Skaffold local k8s, see [LOCAL-K8S.md](LOCAL-K8S.md).

---

## 1. Runtime Preparation

Copy and adjust the local environment files:

```bash
cp local.env .env
cp local.secret.env deploy/k8s/overlays/dev/.local.secret.env
```

Ensure `.env` contains your core app configuration, and the dev overlay secret env has at least:

```bash
DB_URL=postgresql+psycopg://user:pass@host:5432/dbname
```

> These are used both by Docker Compose and by local k8s (via Kustomize/Secrets).

---

## 2. Local Run with Docker Compose

There are two Docker Compose profiles: **dev** and **prod**.

### 2.1 Dev Profile (hot reload, mounted source)

```bash
docker compose --profile dev up
```

- Mounts the source code.
- Runs `uvicorn` with `--reload` for quick iterations.
- Use this when actively changing code.

Stop dev:

```bash
docker compose down --remove-orphans
```

### 2.2 Prod Profile (immutable runtime image)

```bash
docker compose --profile prod up
```

- Uses the same runtime image that would be deployed to k8s.
- No hot reload; treats the container as immutable.
- Use this to approximate production behavior.

---

## 3. Local k8s Run (Minikube + Skaffold, Summary)

See [LOCAL-K8S.md](LOCAL-K8S.md) for detailed steps. At a high level:

```bash
# One-time-ish env bootstrap
make init        # starts Minikube, creates dev namespace, secrets, dev image

# Dev loop (skaffold watches & redeploys)
make dev
```

To tear down the local k8s resources:

```bash
make down        # skaffold delete -p minikube
make k8s-down    # minikube delete -p minikube
```

---

## 4. Health & Diagnostics Endpoints

Once the service is running (via `uvicorn`, Docker, or k8s), you can hit:

### 4.1 Health

```bash
curl -s http://127.0.0.1:8080/api/v1/healthz | jq
```

### 4.2 Config Snapshot

```bash
curl -s http://127.0.0.1:8080/api/v1/configz | jq
```

### 4.3 Version

```bash
curl -s http://127.0.0.1:8080/api/v1/version | jq
```

### 4.4 List Practice Targets

```bash
curl -s http://127.0.0.1:8080/api/v1/targets | jq
```

More details on the API surface live in [API.md](API.md).

---

## 5. Basic “Is it Working?” Checklist

1. **Service starts cleanly**
   - No unhandled exceptions in the console logs.
2. **Health endpoint returns 200**
   - `curl -s -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1:8080/api/v1/healthz`
3. **Config endpoint shows expected values**
   - DB URL, environment name, logging config, etc.
4. **Practice targets are listed**
   - Confirms practice registration and discovery is working.

For production/EKS verification (deployment health, IRSA, DB_URL, writable `/tmp`), see [OPERATIONS.md](OPERATIONS.md) and [EKS.md](EKS.md).
