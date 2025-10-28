# ---- Builder: resolve deps & build app wheel ----
ARG PYTHON_VERSION=3.11.13
FROM python:${PYTHON_VERSION}-slim AS builder
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
FROM python:${PYTHON_VERSION}-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

# Install tini for proper PID 1 signal/child reaping in K8s
# (keeps graceful shutdowns predictable with SIGTERM)
RUN apt-get update && apt-get install -y --no-install-recommends tini ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user (Debian slim uses /usr/sbin/nologin)
RUN useradd -u 10001 -r -s /usr/sbin/nologin appuser

# Update base tools in runtime image
RUN python -m pip install --upgrade "pip>=24.3" "setuptools>=78.1.1" "wheel>=0.43"

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

# Ensure temp goes to /tmp (mounted as emptyDir in K8s if needed)
ENV TMPDIR=/tmp

# Default port is configurable via $PORT; EXPOSE is just documentation
# Use 8080 by default to align with common K8s service targetPort
EXPOSE 8080
ENV PORT=8080

# Container-level healthcheck: K8s will use probes, but this helps when running `docker run`
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import os,sys,urllib.request; port=os.getenv('PORT','8080'); url=f'http://127.0.0.1:{port}/healthz'; \
__import__('urllib.request').urlopen(url, timeout=2).getcode()==200 and sys.exit(0) or sys.exit(1)"

# Run as non-root user
USER appuser

# Use tini as the entrypoint so signals & zombies are handled correctly in K8s
ENTRYPOINT ["/usr/bin/tini", "-g", "--"]

# Uvicorn with overridable concurrency/timeouts for graceful rollouts
CMD ["sh", "-c", "uvicorn cs_fundamentals.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers ${WEB_CONCURRENCY:-2} --timeout-keep-alive 5 --timeout-graceful-shutdown ${GRACEFUL_TIMEOUT:-10}"]
