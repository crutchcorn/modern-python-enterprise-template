"""Scan workspace members and update uv.override_package directives in MODULE.bazel."""

import re
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    import tomli as tomllib  # type: ignore[no-redef]

ROOT = Path(__file__).resolve().parent.parent
MODULE_FILE = ROOT / "MODULE.bazel"

MARKER_START = "# BEGIN uv.override_package workspace members"
MARKER_END = "# END uv.override_package workspace members"


def read_pyproject_name(pyproject: Path) -> str | None:
    """Read the project name from a pyproject.toml."""
    try:
        data = tomllib.loads(pyproject.read_text())
        return data.get("project", {}).get("name")
    except (OSError, tomllib.TOMLDecodeError):
        return None


def detect_bazel_target(member_dir: Path, pkg_name: str) -> str | None:
    """Determine the Bazel target label for a workspace member.

    Convention:
      - Python source package: packages/{dir}/src/{name}/__init__.py  -> //packages/{dir}/src/{name}
      - Python app:            apps/{dir}/main.py                     -> //apps/{dir}
      - JS/TS frontend build:  {dir}/vite.config.ts                   -> //{rel}:build
      - JS/TS package:         packages/{dir}/package.json            -> //packages/{dir}
    """
    rel = member_dir.relative_to(ROOT)

    # Python source package under src/
    init = member_dir / "src" / pkg_name / "__init__.py"
    if init.exists():
        return f"//{rel}/src/{pkg_name}"

    # Python app (has main.py)
    if (member_dir / "main.py").exists():
        return f"//{rel}"

    # JS/TS frontend with vite build target
    if (member_dir / "vite.config.ts").exists():
        return f"//{rel}:build"

    # JS/TS package (has package.json, no Python source)
    if (member_dir / "package.json").exists():
        return f"//{rel}"

    return None


def find_workspace_overrides() -> list[tuple[str, str]]:
    """Return (name, target) pairs for all workspace members."""
    overrides: list[tuple[str, str]] = []

    root_pyproject = ROOT / "pyproject.toml"
    root_name = read_pyproject_name(root_pyproject)
    if root_name:
        overrides.append((root_name, "//:root"))

    for search_dir in [ROOT / "apps", ROOT / "packages"]:
        if not search_dir.is_dir():
            continue
        for member_dir in sorted(search_dir.iterdir()):
            pyproject = member_dir / "pyproject.toml"
            if not pyproject.exists():
                continue
            name = read_pyproject_name(pyproject)
            if not name:
                continue
            target = detect_bazel_target(member_dir, name)
            if target:
                overrides.append((name, target))

    return overrides


def generate_override_lines(overrides: list[tuple[str, str]]) -> list[str]:
    """Generate the Starlark lines for uv.override_package calls."""
    lines: list[str] = []
    for name, target in overrides:
        lines.append(f'uv.override_package(name = "{name}", lock = "//:uv.lock", target = "{target}")')
    return lines


def update_module_file(override_lines: list[str]) -> None:
    """Replace the override block in MODULE.bazel with the new lines."""
    content = MODULE_FILE.read_text()

    block = MARKER_START + "\n" + "\n".join(override_lines) + "\n" + MARKER_END

    pattern = re.compile(
        rf"^{re.escape(MARKER_START)}$.*?^{re.escape(MARKER_END)}$",
        re.MULTILINE | re.DOTALL,
    )

    if pattern.search(content):
        new_content = pattern.sub(block, content)
    else:
        raise RuntimeError(
            f"Could not find marker block in {MODULE_FILE}.\n"
            f"Add these markers where overrides should go:\n"
            f"  {MARKER_START}\n"
            f"  {MARKER_END}"
        )

    MODULE_FILE.write_text(new_content)


def main() -> None:
    overrides = find_workspace_overrides()
    if not overrides:
        print("No workspace members found.")
        return

    override_lines = generate_override_lines(overrides)
    update_module_file(override_lines)

    print(f"Updated {MODULE_FILE.name} with {len(overrides)} workspace overrides:")
    for name, target in overrides:
        print(f"  {name} -> {target}")


if __name__ == "__main__":
    main()
