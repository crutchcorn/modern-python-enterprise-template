# Build from repo root: docker build -f apps/backend/Dockerfile .

# Stage 1: Build mypyc extensions with Bazel (needs glibc for Bazel)
FROM ghcr.io/astral-sh/uv:debian-slim AS builder

# Install system dependencies for Bazel and compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    clang \
    curl \
    gcc \
    g++ \
    git \
    patch \
    && rm -rf /var/lib/apt/lists/*

# Install Python version specified in .python-version
COPY .python-version .
RUN uv python install

# Install Bazelisk (manages Bazel versions automatically)
ARG TARGETARCH
RUN curl -fsSL -o /usr/local/bin/bazel \
    "https://github.com/bazelbuild/bazelisk/releases/latest/download/bazelisk-linux-${TARGETARCH}" \
    && chmod +x /usr/local/bin/bazel

WORKDIR /workspace

# Copy the full workspace (Bazel needs the full source tree)
COPY . .

# Build backend and shared mypyc extensions with Bazel
RUN bazel build //apps/backend/... //packages/...

# Deploy compiled .so files into source packages
RUN uv run python tools/deploy_mypyc.py

# Stage 2: Slim runtime image
FROM ghcr.io/astral-sh/uv:debian-slim AS runtime

# Install build tools needed to compile C extensions (e.g. httptools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    clang \
    && rm -rf /var/lib/apt/lists/*

# Install Python version specified in .python-version
COPY .python-version .
RUN uv python install

WORKDIR /workspace

# Copy workspace-level files needed for uv resolution
COPY pyproject.toml uv.lock ./

# Copy the shared package (with mypyc .so from builder)
COPY packages/shared packages/shared
COPY --from=builder /workspace/packages/shared/src/shared/*.so packages/shared/src/shared/

# Copy the backend app
COPY apps/backend apps/backend

# Install dependencies in production mode
RUN uv sync --frozen --no-dev --package backend

WORKDIR /workspace/apps/backend

EXPOSE 8000

ENV PYTHON_GIL=0

CMD ["uv", "run", "fastapi", "run", "--host", "0.0.0.0"]
