# DEVELOPER - Local Dev Environment

This guide covers local development.

---

## 1. Requirements

Core tooling:

- **Python**: 3.11+
  - <https://docs.python.org/3/>
  - <https://www.python.org/downloads/>
- **uv** (package + venv manager)
  - <https://docs.astral.sh/uv/>
  - <https://github.com/astral-sh/uv>
- **pre-commit**
  - <https://pre-commit.com/>
  - <https://github.com/pre-commit/pre-commit>

Recommended tooling:

- Docker & Docker Compose
- `jq` for JSON filtering
- `yq` for YAML filtering
- Minikube + Skaffold (for local k8s workflows)
- `kustomize` (if not present via `kubectl kustomize`)

---

## 2. Initial Setup

Install dependencies:

```bash
uv sync
```

Install `pre-commit` and hooks:

```bash
uv tool install pre-commit
pre-commit install
```

Update uv when needed:

```bash
uv self update
```

### 2.1 Managing Dependencies with uv

Add a new dependency:

```bash
uv add ruff
```

Refresh the lockfile with latest version of all dependencies:

```bash
uv lock --upgrade
```

Sync dependencies into the venv:

```bash
uv sync              # App deps
uv sync --group dev  # Dev/Test tooling
```

Inspect installed packages:

```bash
uv pip list
```

---

## 3. Linting, Formatting & Type Checking

The main entry point for all linting/type checking is the `lint` target:

```bash
make lint
```

Which is equivalent to:

```bash
uv run mypy --show-error-codes --pretty .
uv run ruff check .
uv run ruff format .
```

You can also run individual commands:

- Lint only (no fixes):

  ```bash
  uv run ruff check .
  ```

- Lint with autofix:

  ```bash
  uv run ruff check . --fix
  ```

- Format (check only):

  ```bash
  uv run ruff format . --check
  ```

- Format and apply:

  ```bash
  uv run ruff format .
  ```

- Type checking:

  ```bash
  uv run mypy --show-error-codes --pretty .
  ```

Running `pre-commit` manually over the whole repo:

```bash
pre-commit run --all-files
```

---

## 4. Tests

The canonical entrypoint for tests is:

```bash
make tests
```

Under the hood:

```bash
uv run pytest -q
```

More granular test commands:

- All tests, verbose:

  ```bash
  uv run pytest -v
  ```

- All tests after clearing cache:

  ```bash
  uv run pytest -v --cache-clear
  ```

- All tests, suppressing warnings:

  ```bash
  uv run pytest -p no:warnings
  ```

- Package:

  ```bash
  uv run pytest -v automation/test_data_structures
  ```

- Single test module:

  ```bash
  uv run pytest -vv automation/test_data_structures/test_graph.py
  ```

- Single test method from a class:

  ```bash
  uv run pytest -vv automation/test_data_structures/test_graph.py -k test_problem_number_of_islands_2
  ```

- Single test function from a module:

  ```bash
  uv run pytest -vv automation/core/test_inject.py::test_compile_functions_single_and_multiple_with_recursion_and_crosscalls
  ```

> IDE tip: In VSCode or PyCharm, right‑click a test file or class and choose “Run tests”, or use keybindings such as `Ctrl+Shift+F10`.

---

## 5. Type Inference with MonkeyType

**MonkeyType** infers and applies type hints from **runtime traces** collected during test runs.
It complements `mypy` by quickly filling in missing annotations.

### 5.1 Reset Traces

Recommended before fresh runs:

```bash
rm -rf .monkeytype
rm -f monkeytype.sqlite3
```

### 5.2 Collect Traces

Use pytest’s importlib mode so tests are imported as packages (fully qualified names):

```bash
PYTEST_ADDOPTS="--import-mode=importlib -q" uv run monkeytype run -m pytest
```

List captured modules:

```bash
uv run monkeytype list-modules
```

You should see fully qualified names, e.g.:

```text
automation.test_core.test_validation
cs_fundamentals.core.validation
cs_fundamentals.data_structures.stack
```

### 5.3 Apply Inferred Types

Preview a stub for a module:

```bash
uv run monkeytype stub cs_fundamentals.core.validation
```

Apply types directly:

```bash
uv run monkeytype apply cs_fundamentals.core.validation
```

Apply to everything captured:

```bash
uv run monkeytype list-modules | xargs -n1 uv run monkeytype apply
```

### 5.4 Tidy & Verify

After applying hints:

```bash
uv run ruff check . --fix
uv run ruff format .
uv run mypy .
```

---

## 6. Local App Runners (Dev vs. Prod)

For a quick dev run:

```bash
kubectl config use-context minikube
make init
make dev
```

For containerized runs, see [RUNBOOK.md](RUNBOOK.md). For Minikube/Skaffold, see [LOCAL-K8S.md](LOCAL-K8S.md).

---

## 7. Where to Go Next

- **Operational behavior**: [OPERATIONS.md](OPERATIONS.md)
- **Security & scanning**: [SECURITY.md](SECURITY.md)
- **CI/CD mechanics**: [CI_CD.md](CI_CD.md)
