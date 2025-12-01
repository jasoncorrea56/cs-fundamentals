# cs-fundamentals

[![CI Status](https://github.com/jasoncorrea56/cs-fundamentals/actions/workflows/automation.yaml/badge.svg)](https://github.com/jasoncorrea56/cs-fundamentals/actions/workflows/automation.yaml)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)
![Ruff](https://img.shields.io/badge/code%20style-ruff-black?logo=ruff&logoColor=white)
![Semgrep](https://img.shields.io/badge/security-semgrep-blue?logo=semgrep&logoColor=white)
![Trivy](https://img.shields.io/badge/vulnerability%20scan-trivy-red?logo=trivy&logoColor=white)
![SBOM](https://img.shields.io/badge/SBOM-syft-yellow?logo=linux&logoColor=white)
![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009485?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/docker-ready-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/kubernetes-1.34-blue?logo=kubernetes&logoColor=white)
![Helm](https://img.shields.io/badge/Helm-chart-0F1689?logo=helm&logoColor=white)
![AWS ECR](https://img.shields.io/badge/AWS-ECR-orange?logo=amazon-aws&logoColor=white)
![AWS EKS](https://img.shields.io/badge/AWS-EKS-orange?logo=amazon-eks&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-modular-7B42BC?logo=terraform&logoColor=white)
![License: Apache-2.0 OR MIT](https://img.shields.io/badge/license-Apache--2.0%20OR%20MIT-green)

**cs-fundamentals** is a practice and reference project for computer science fundamentals:

- Data structures, algorithms, and problem‑solving patterns
- A FastAPI backend that exposes practice/evaluation endpoints
- A full production‑grade toolchain (tests, static analysis, containerization, k8s, EKS, CI/CD)

The goal is twofold:

1. Provide a tight feedback loop for practicing CS fundamentals.
2. Showcase professional‑grade engineering, DevOps, and runtime operations.

---

## Quickstart

If you just want to see the service running locally with the simplest path:

```bash
uv sync
cp local.env .env
docker compose --profile dev up
```

Then:

```bash
curl -s http://127.0.0.1:8080/api/v1/healthz | jq
```

For richer local/dev flows (Minikube, Skaffold, & Makefile helpers), see:

- [RUNBOOK.md](RUNBOOK.md) - Run the service and call the API
- [LOCAL-K8S.md](LOCAL-K8S.md) - Minikube + Skaffold workflow
- [DEVELOPER.md](DEVELOPER.md) - Full local dev environment

---

## Documentation Map

This repo is documented as a small “docs suite” rather than one mega‑README:

1. **[README.md](README.md)** - Project overview and entry points
2. **[RUNBOOK.md](docs/RUNBOOK.md)** - “Do this now” guide for running and hitting the API
3. **[DEVELOPER.md](docs/DEVELOPER.md)** - Dev environment, tooling, linting, tests, & type‑hints
4. **[TECH.md](docs/TECH.md)** - Architecture, processes, logging, & configuration model
5. **[KUBERNETES.md](docs/KUBERNETES.md)** - Helm chart, manifests, & k8s deployment model
6. **[CI_CD.md](docs/CI_CD.md)** - CI workflows, build/release, & blue‑green + canary CD
7. **[EKS.md](docs/EKS.md)** - AWS EKS setup, Secrets Manager, CSI/IRSA, & Terraform wiring
8. **[API.md](docs/API.md)** - FastAPI surface + example `curl` calls
9. **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - How to contribute, code style, & review expectations
10. **[SECURITY.md](docs/SECURITY.md)** - Static analysis, vuln scanning, & secrets handling
11. **[OPERATIONS.md](docs/OPERATIONS.md)** - Runtime knobs, logging, & operational checks
12. **[MAKEFILE.md](docs/MAKEFILE.md)** - Make targets and how to use them
13. **[LOCAL-K8S.md](docs/LOCAL-K8S.md)** - Local k8s via Minikube + Skaffold

---

## High‑Level Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI (0.115+)
- **Packaging/env**: `uv`
- **Testing**: `pytest`
- **Code quality**: `ruff`, `mypy`, `pre-commit`
- **Security & SBOM**: OSV scanner, Semgrep, Trivy, Syft
- **Containers**: Docker, Docker Compose (dev + prod profiles)
- **Orchestration**: Kubernetes 1.34, Helm chart, Skaffold dev loop
- **Cloud**: AWS ECR + EKS, AWS Secrets Manager via Secrets Store CSI + IRSA
- **Infra as Code**: Terraform (modular app chart + cluster infra)
- **CI/CD**: GitHub Actions with build, scan, and EKS deploy (blue‑green + canary)

For specific commands and detailed flows, follow the links in the documentation map above.

## Contributing

This project is not open to external contributions. It is maintained as a personal and portfolio codebase.

## License

This project is **dual-licensed** under:

- **Apache License 2.0**
- **MIT License**

You may choose **either** license when using this software.

See the [LICENSE](LICENSE) and [NOTICE](NOTICE) files for details.
