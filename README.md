# Template Features

- UV for Python dependency management
- MyPy for static type checking
- Ruff for linting and formatting
- Bazel monorepo for cached Python apps and packages builds and tests
- MyPyC for compiling Python code to C for improved performance
- GIL-free Python code for better concurrency
- PyTest for testing

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