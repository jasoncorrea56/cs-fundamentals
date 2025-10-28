MINIKUBE_PROFILE ?= minikube

.PHONY: k8s-up
k8s-up:
	@minikube start -p $(MINIKUBE_PROFILE) --cpus=4 --memory=6g \
		--dns-proxy=true \
		--driver=docker \
		--docker-opt=dns=8.8.8.8 \
		--docker-opt=dns=1.1.1.1

.PHONY: k8s-env
k8s-env:
	@eval $$(minikube -p $(MINIKUBE_PROFILE) docker-env) && echo "Docker env configured for Minikube"

.PHONY: dev
dev:
	@skaffold dev -p minikube

.PHONY: dev-in-node
dev-in-node:
	@eval $$(minikube -p $(MINIKUBE_PROFILE) docker-env) && skaffold dev -p minikube

.PHONY: down
down:
	@skaffold delete -p minikube || true

.PHONY: k8s-down
k8s-down:
	@minikube delete -p $(MINIKUBE_PROFILE)

.PHONY: lint
lint:
	@uv run mypy --show-error-codes --pretty .
	@uv run ruff check .
	@uv run ruff format .

.PHONY: semgrep
semgrep:
	@uv run semgrep ci --verbose --config p/ci --config p/security-audit --config p/python --json | jq '.results[] | {check_id, path, start: .start.line, message}'

.PHONY: semgrep-strict
semgrep-deep:
	@uv run semgrep ci --verbose --config p/ci --config p/security-audit --config p/python --sarif

.PHONY: tests
tests:
	@uv run pytest -q
