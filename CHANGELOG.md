# Changelog

## [0.8.0](https://github.com/jasoncorrea56/cs-fundamentals/compare/v0.7.2...v0.8.0) (2025-12-02)


### Features

* add QA environment support and update licensing ([7776c05](https://github.com/jasoncorrea56/cs-fundamentals/commit/7776c0564a331a5e2cf15f3295c2a50c09d93717))
* **ci:** implement unified 3-env CI/CD (Dev/QA/Prod) with PR-only CI, push-based CD, and deploy-only manual workflow ([08b5423](https://github.com/jasoncorrea56/cs-fundamentals/commit/08b5423341d2eab9e78433d31f2ced73cb4d9a33))
* **helm:** add dev values and refine ALB ingress for EKS dev env ([8db012a](https://github.com/jasoncorrea56/cs-fundamentals/commit/8db012a5ebc06ab06522db950514eadb7e9bdf0c))
* **helm:** consolidate base+env values and standardize TLS ([da221d6](https://github.com/jasoncorrea56/cs-fundamentals/commit/da221d6c487db796b0bc9d7087c8801ea3cba871))
* **helm:** finalize dev ingress via ALB on csf-dev.jasoncorrea.dev ([959b9c6](https://github.com/jasoncorrea56/cs-fundamentals/commit/959b9c6c6208a1651774653fae43877ae2397aba))


### Bug Fixes

* include environment overlays in CD Helm args ([9216d27](https://github.com/jasoncorrea56/cs-fundamentals/commit/9216d272df0a461844332feb20c3d0c18fa1e898))
* remove quotes ([9ea6a6a](https://github.com/jasoncorrea56/cs-fundamentals/commit/9ea6a6a6d8d3457204c4fa48f411952577f8186d))


### Documentation

* updated CI/CD doc ([e9b0533](https://github.com/jasoncorrea56/cs-fundamentals/commit/e9b0533ba1aee0d092fb278bd5e26009eb090539))

## [0.7.2](https://github.com/jasoncorrea56/cs-fundamentals/compare/v0.7.1...v0.7.2) (2025-11-15)


### Bug Fixes

* add release-please json config and cleanup ([db8cafb](https://github.com/jasoncorrea56/cs-fundamentals/commit/db8cafb322e190f1fa23506df59167de18ff33d0))
* remove latest tag to fix ECR collision ([b468a91](https://github.com/jasoncorrea56/cs-fundamentals/commit/b468a9106e462e133aa961b551ac8e1366d615e8))

## 0.1.0 (2025-11-15)


### Features

* **12factor:** factor 1 - all deps pinned and ruff linting and formatting in place ([44dcd40](https://github.com/jasoncorrea56/cs-fundamentals/commit/44dcd408f366f37c4b8952723dd105f580b4d463))
* **12factor:** factor 3 - load app version from pyproject.toml and wire settings into FastAPI app ([338f379](https://github.com/jasoncorrea56/cs-fundamentals/commit/338f37977caa5c82f42f03d43ab551f5625ea3d6))
* **acm_cert:** configure Ingress for HTTPS via ALB and ACM cert with ExternalDNS integration ([38cd51a](https://github.com/jasoncorrea56/cs-fundamentals/commit/38cd51ada25de9b86f9eaa5494ebc6613a4cde79))
* add CI lint and test workflow, configure uv build system ([3bac6f5](https://github.com/jasoncorrea56/cs-fundamentals/commit/3bac6f557edc3b21a420e13b5b22e39d1a7d1828))
* add FastAPI and build REST API wrapper around core logic ([35808bc](https://github.com/jasoncorrea56/cs-fundamentals/commit/35808bce932272c51607ff8af455abea12fc91fc))
* add pre-commit and cleanup ([05a9982](https://github.com/jasoncorrea56/cs-fundamentals/commit/05a9982fbed8f18986fc1712beb5092f8f439770))
* add UV support for env and package mgmt ([d3d5902](https://github.com/jasoncorrea56/cs-fundamentals/commit/d3d59022fdfeda692b0c215cc05a28b51ca61fa8))
* **admin:** factor 12 - add support for one-off admin processes ([8388949](https://github.com/jasoncorrea56/cs-fundamentals/commit/8388949246d0ea11a85f65b8b33213ccbf27d47f))
* **concurrency:** factor 8 - add WEB_CONCURRENCY workers, Procfile, and README scaling notes ([154faf7](https://github.com/jasoncorrea56/cs-fundamentals/commit/154faf74b1087d4c5cad206feed8772ff332f0bf))
* **disposability:** factor 9 - add graceful shutdown, explicit stop window, and time-limited test runs ([5210b1b](https://github.com/jasoncorrea56/cs-fundamentals/commit/5210b1bb585f6c5c9a3b92bbf4e87c5e6f807f27))
* **docker:** factor 5 — containerized, dev/prod Compose, hot reload, GH build pipeline ([763ae5d](https://github.com/jasoncorrea56/cs-fundamentals/commit/763ae5d5f4c9ff52b7a5e1a7604e7ebf151475c0))
* **eks:** Helm updates to add ALB ingress, externalize image repo/tag & use existing SA csf-app ([4c550d4](https://github.com/jasoncorrea56/cs-fundamentals/commit/4c550d4bed88856e0c4159a8e52a32b16c18f9c3))
* **factor6:** factor 6 — stateless processes, multi-worker uvicorn, read-only FS with /tmp, and graceful lifespan hooks ([148e5af](https://github.com/jasoncorrea56/cs-fundamentals/commit/148e5afc6743a98f649be798e4c56186ad02d8f7))
* **helm:** add Helm chart and integrate Skaffold Helm deploy workflow ([b289edc](https://github.com/jasoncorrea56/cs-fundamentals/commit/b289edc4dafbc973acb27a55183004ef17314544))
* **helm:** add weighted canary/blue-green rollout for cs-fundamentals ([f4dd04a](https://github.com/jasoncorrea56/cs-fundamentals/commit/f4dd04a09542fe072f75ae3fc48d470590791ced))
* **helm:** add zero-downtime RollingUpdate + PodDisruptionBudget defaults ([3dec426](https://github.com/jasoncorrea56/cs-fundamentals/commit/3dec426e523d231b9eabae26693514b84eb3178d))
* **helm:** harden deployment config with probes, resource limits, and security contexts ([f3613de](https://github.com/jasoncorrea56/cs-fundamentals/commit/f3613de42a005f57539c4b425ec66fc3022a92ec))
* **helm:** prod-grade config & secret wiring (ASM/CSI via IRSA), harden FS and local dev overlay support ([0543b1d](https://github.com/jasoncorrea56/cs-fundamentals/commit/0543b1dfe6bf7b918b7113f17dd11d9e5de4ace7))
* **helm:** wire prod HPA v2 + behavior and align with EKS metrics ([0201379](https://github.com/jasoncorrea56/cs-fundamentals/commit/0201379c406f9fd6c7f039821084840fe37d5da2))
* **k8s:** add Kubernetes dev environment with Minikube, Skaffold, and K8s manifests for local deployment ([9602f77](https://github.com/jasoncorrea56/cs-fundamentals/commit/9602f77c17fb12fc6733cf25d56fb3bdeb77d302))
* **logging:** add structured application-wide logging with request middleware ([1ee328f](https://github.com/jasoncorrea56/cs-fundamentals/commit/1ee328fbf54044135323e597825c4df227ea1f10))
* **logs:** factor 11 - implement structured request logging and request ID propagation ([d044800](https://github.com/jasoncorrea56/cs-fundamentals/commit/d0448003e3472f524f0ba4ca76b6ccc61cd80475))
* **parity:** factor 10 - pin Python 3.11.13 across dev/CI/prod, add .python-version, and container smoke test ([6bd9d20](https://github.com/jasoncorrea56/cs-fundamentals/commit/6bd9d205963103ebb220878e837bea84aa888f7a))
* **port-binding:** factor 7 - runtime port configurable via  and add container healthcheck ([13e4791](https://github.com/jasoncorrea56/cs-fundamentals/commit/13e4791677a83f8e59b6e24dac4a8ed1ee0914eb))
* **security:** add pod/container securityContext, optional secrets-store and /tmp mounts, and fix envFrom rendering ([25ffeb8](https://github.com/jasoncorrea56/cs-fundamentals/commit/25ffeb8c835a349c9091e3693b223e969718ae02))
* **typecheck:** integrate mypy type-checking with Ruff and CI workflow ([f2aafc2](https://github.com/jasoncorrea56/cs-fundamentals/commit/f2aafc2e1f7c8441ebcaeafd2abec16d7f08ca50))


### Bug Fixes

* **cd:** harden canary smoke Pod to fully satisfy PodSecurity Restricted ([d228764](https://github.com/jasoncorrea56/cs-fundamentals/commit/d2287645af13789e885ea63bebeb9bf8a052a6c1))
* **cd:** replace  canary smoke test with Pod manifest compliant with PodSecurity Restricted ([340c000](https://github.com/jasoncorrea56/cs-fundamentals/commit/340c000f4832a60a66b4ab22fc749861ac4abd01))
* **cd:** replace kubectl run canary probe with Pod manifest compliant w/ PodSecurity ([6ee0a85](https://github.com/jasoncorrea56/cs-fundamentals/commit/6ee0a8582ce33dcc0da15277e12b5e7e4abb3c7d))
* post-12 Factor QA - correct error handling for negative/failed tests and minor response refactor for consistency ([3234261](https://github.com/jasoncorrea56/cs-fundamentals/commit/3234261f19ccbf2191e32d8d5c1ed53b37f14043))
* test fix from CI ([119fbe8](https://github.com/jasoncorrea56/cs-fundamentals/commit/119fbe8baec8229176f251c0e1f638a2c7fc624a))


### Documentation

* refactored README into docs suite ([8635d2b](https://github.com/jasoncorrea56/cs-fundamentals/commit/8635d2be93c56d0d2aaa9c915a34470697d88844))
