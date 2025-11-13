MINIKUBE_PROFILE ?= minikube
DEV_NS           ?= csf-dev
DEV_RELEASE      ?= csf
DEV_ENV_PRIMARY  ?= deploy/k8s/overlays/dev/.local.secret.env

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

.PHONY: dev-namespace
dev-namespace:
	kubectl create namespace $(DEV_NS) --dry-run=client -o yaml | kubectl apply -f -

.PHONY: dev-image
dev-image:
	# Build the dev image inside Minikube's Docker daemon so pulls succeed
	eval "$$(minikube docker-env)" && docker build -t cs-fundamentals:dev .

.PHONY: dev-secrets
dev-secrets: dev-namespace
	# Strict mode: only accept the overlay-local file; no fallbacks.
	@if [ ! -f "$(DEV_ENV_PRIMARY)" ]; then \
		printf '%s\n%s\n  %s\n' \
		  "ERROR: Missing secret env file for dev." \
		  "Create it with at least the DB_URL line at:" \
		  "$(DEV_ENV_PRIMARY)"; \
		exit 1; \
	fi
	# Declaratively create/update the Secret from the overlay-local env file
	@( \
		if command -v kustomize >/dev/null 2>&1; then \
			kustomize build deploy/k8s/overlays/dev; \
		else \
			kubectl kustomize deploy/k8s/overlays/dev; \
		fi \
	) | kubectl apply -f -

.PHONY: dev-install
dev-install: dev-image dev-secrets
	helm upgrade --install $(DEV_RELEASE) ./helm \
		-f helm/values-minikube.yaml \
		-n $(DEV_NS) --create-namespace --wait --timeout 5m

.PHONY: dev-setup
dev-setup: dev-install

init:
	@echo "🚀 Starting local environment..."
	make k8s-up
	@echo "✅ Minikube started."

	@echo "🔧 Setting up Dev namespace..."
	make dev-namespace
	@echo "✅ Local Dev namespace ready."

	@echo "🔧 Setting up Dev secrets..."
	make dev-secrets
	@echo "✅ Local Dev secrets ready."

	@echo "🌱 Building Dev image..."
	make dev-image
	@echo "🎉 Initialization complete!"

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
