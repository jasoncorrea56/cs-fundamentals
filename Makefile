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
	@export DB_URL="$(grep -E '^DB_URL=' .env | cut -d= -f2-)"
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

.PHONY: verify
verify:
	@echo "🔍 Verifying cs-fundamentals deployment in namespace 'csf'..."
	@echo "\n✅ Checking deployment and pods..."
	kubectl -n csf get deploy,rs,pods
	@echo "\n✅ Checking deployment conditions..."
	kubectl -n csf describe deploy csf-cs-fundamentals | grep -A5 "Conditions" || true
	@echo "\n✅ Checking health endpoint..."
	@if kubectl -n csf get svc csf-cs-fundamentals >/dev/null 2>&1; then \
		curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8080/api/v1/healthz || true; \
	fi
	@echo "\n✅ Checking environment variables..."
	kubectl -n csf exec -it deploy/csf-cs-fundamentals -- printenv | grep -E 'DB_URL|TMPDIR' || true
	@echo "\n✅ Checking writable /tmp..."
	kubectl -n csf exec -it deploy/csf-cs-fundamentals -- sh -c 'touch /tmp/testfile && ls -l /tmp/testfile' || true
	@echo "\n✅ Helm chart lint and manifest check..."
	helm lint ./helm
	@helm get manifest csf -n csf | head -n 30 || true
	@echo "\n🎯 Verification complete!"
