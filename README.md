# Install

- Install Bazelisk: https://github.com/bazelbuild/bazelisk?tab=readme-ov-file#installation
- Install UV: https://docs.astral.sh/uv/getting-started/installation/

```shell
bazel # To install Bazel via Bazelisk
uv tool install poethepoet
uv tool install ruff
```

# Usage

```shell
poe # List all tasks
```

## Bazel

```shell
bazel build //packages/shared/src/shared  # Build the shared library
bazel build //apps/backend                 # Build the backend app
bazel run //:generate_requirements_lock    # Update pip lock file via uv
```