# Modern Python Enterprise Template

This is a template for modern Python enterprise applications, featuring a monorepo structure with a Python backend and a React frontend. The template includes various tools and optimizations for development, testing, and deployment.

You can check out the live demos here:

- [Backend API Documentation](https://modern-python-enterprise-template.onrender.com/docs)
- [Frontend Application](https://modern-python-enterprise-template.netlify.app)

## Template Features

- UV for Python dependency management
- MyPy for static type checking
- Ruff for linting and formatting
- Bazel monorepo for cached Python apps and packages builds and tests
- MyPyC for compiling Python code to C for improved performance
- GIL-free Python code for better concurrency
- PyTest for testing
- React frontend and monorepo packages for shared components and utilities
    - Connected with Bazel for cached builds and tests
    - ESLint for linting
    - Prettier for formatting
    - Vite for building and development server
    - Vitest Browser Mode for real-world in-browser integration testing
    - Auto-generated types for TypeScript from the FastAPI schema
- CI pipeline for running tests and linting on both backend and frontend with caching and other optimizations
- Sentry for error tracking both in the backend and frontend
- Per-branch deployments via Render and Netlify

## Install

- [Install Bazelisk](https://github.com/bazelbuild/bazelisk?tab=readme-ov-file#installation)
- [Install UV](https://docs.astral.sh/uv/getting-started/installation/)
- [Install Node](https://nodejs.org/en/download) 

```shell
bazel # To install Bazel via Bazelisk
uv tool install poethepoet
uv tool install ruff
corepack enable # To install PNPM via Node
```

## Usage

```shell
poe # List all backend-related tasks
pnpm run # List all frontend-related scripts
```

### Bazel

When a new dependency or app is added to the project (either via `uv` or a new package added to the monorepo), run the following command at root to update Bazel's resolves:

```shell
poe sync
```
