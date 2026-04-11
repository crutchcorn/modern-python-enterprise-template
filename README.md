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

When a new dependency is added to the project (either via `uv` or a new package added to the monorepo), run the following command at root to update Bazel's resolves:

```shell
poe sync
```