FROM mcr.microsoft.com/devcontainers/python:3.11.13

# Dev tools
RUN pipx install uv && pip install --no-cache-dir pre-commit

# Optional: faster installs across container recreations
VOLUME /root/.cache/uv

WORKDIR /workspaces/cs-fundamentals
