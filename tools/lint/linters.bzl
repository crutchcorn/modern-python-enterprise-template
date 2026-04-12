"Define linter aspects for the repository"

load("@aspect_rules_lint//lint:eslint.bzl", "lint_eslint_aspect")
load("@aspect_rules_lint//lint:lint_test.bzl", "lint_test")
load("@aspect_rules_lint//lint:ruff.bzl", "lint_ruff_aspect")

ruff = lint_ruff_aspect(
    binary = Label("@aspect_rules_lint//lint:ruff_bin"),
    configs = [
        Label("@//:pyproject.toml"),
    ],
)

ruff_test = lint_test(aspect = ruff)

eslint_frontend = lint_eslint_aspect(
    binary = Label("//tools/lint:eslint_frontend"),
    configs = [
        Label("//apps/frontend:eslintrc"),
    ],
)

eslint_frontend_test = lint_test(aspect = eslint_frontend)

eslint_components = lint_eslint_aspect(
    binary = Label("//tools/lint:eslint_components"),
    configs = [
        Label("//packages/components:eslintrc"),
    ],
)

eslint_components_test = lint_test(aspect = eslint_components)
