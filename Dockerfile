# ---- Builder: resolve deps & build app wheel ----
FROM python:3.11-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Install build tooling and uv (for export), then cache deps by lockfile
RUN pip install --no-cache-dir build pipx && pipx install uv

# Ensure uv is on PATH
ENV PATH="/root/.local/bin:${PATH}"

# Copy just manifests first to maximize cache hits
COPY pyproject.toml uv.lock /app/

# Export pinned deps, then remove:
#  - the editable project line (-e .)
#  - hash pins (pip wheel + --require-hashes don't mix with editables)
RUN uv export --no-dev --format requirements-txt -o /tmp/requirements.txt
RUN grep -vE '^\s*-e\s+\.$' /tmp/requirements.txt \
  | sed -E 's/ --hash=[^ ]+//g' \
  > /tmp/requirements.clean.txt

# Prebuild third-party wheels only
RUN pip wheel --wheel-dir /wheels -r /tmp/requirements.clean.txt

# Now copy the source and build the app wheel
COPY . /app/
RUN python -m build --wheel --outdir /dist


# ---- Runtime: minimize runtime image size by installing wheels only ----
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Create non-root user
RUN useradd -u 10001 -r -s /sbin/nologin appuser

# Install deps wheels from builder
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Install the app wheel from builder
COPY --from=builder /dist/ /tmp/dist/
RUN pip install --no-cache-dir /tmp/dist/*.whl && rm -rf /tmp/dist

# Copy test files
COPY pyproject.toml /app/pyproject.toml
COPY automation /automation
ENV TEST_ROOT=/automation

# Ensure temp goes to /tmp (tmpfs in prod compose)
ENV TMPDIR=/tmp

# Run as non-root user
USER appuser
EXPOSE 8000
CMD ["uvicorn", "cs_fundamentals.main:app", "--host", "0.0.0.0", "--port", "8000"]
