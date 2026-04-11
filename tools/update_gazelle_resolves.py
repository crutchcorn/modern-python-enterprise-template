"""Scan packages/*/src/*/ for Python packages and update gazelle:resolve directives in the root BUILD.bazel."""

import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGES_DIR = ROOT / "packages"
BUILD_FILE = ROOT / "BUILD.bazel"

RESOLVE_MARKER_START = "# BEGIN gazelle:resolve local packages"
RESOLVE_MARKER_END = "# END gazelle:resolve local packages"


def find_local_packages() -> dict[str, str]:
    """Return a mapping of Python package name -> Bazel label for all local packages."""
    packages: dict[str, str] = {}
    if not PACKAGES_DIR.exists():
        return packages

    for pkg_dir in sorted(PACKAGES_DIR.iterdir()):
        src_dir = pkg_dir / "src"
        if not src_dir.is_dir():
            continue
        for py_pkg in sorted(src_dir.iterdir()):
            init_file = py_pkg / "__init__.py"
            if not init_file.exists():
                continue
            pkg_name = py_pkg.name
            label = f"//packages/{pkg_dir.name}/src/{pkg_name}"
            packages[pkg_name] = label
    return packages


def collect_exports(init_file: Path) -> list[str]:
    """Parse __init__.py and collect exported names (functions, classes, assignments)."""
    try:
        tree = ast.parse(init_file.read_text())
    except SyntaxError:
        return []
    names: list[str] = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.append(target.id)
    return sorted(names)


def generate_resolve_lines(packages: dict[str, str]) -> list[str]:
    """Generate gazelle:resolve comment lines for all local packages and their exports."""
    lines: list[str] = []
    for pkg_name, label in sorted(packages.items()):
        lines.append(f"# gazelle:resolve py {pkg_name} {label}")
        init_file = ROOT / label.lstrip("/") / "__init__.py"
        for name in collect_exports(init_file):
            lines.append(f"# gazelle:resolve py {pkg_name}.{name} {label}")
    return lines


def update_build_file(resolve_lines: list[str]) -> None:
    """Replace the resolve block in BUILD.bazel with the new lines."""
    content = BUILD_FILE.read_text()

    block = f"{RESOLVE_MARKER_START}\n" + "\n".join(resolve_lines) + f"\n{RESOLVE_MARKER_END}"

    pattern = re.compile(
        rf"^{re.escape(RESOLVE_MARKER_START)}$.*?^{re.escape(RESOLVE_MARKER_END)}$",
        re.MULTILINE | re.DOTALL,
    )

    if pattern.search(content):
        new_content = pattern.sub(block, content)
    else:
        # Insert after the load() statements
        old_lines = content.split("\n")
        insert_idx = 0
        for i, line in enumerate(old_lines):
            if line.startswith("load("):
                insert_idx = i + 1
            elif line.startswith("# gazelle:resolve"):
                # Remove old hard-coded resolve lines
                old_lines[i] = ""
        # Clean up blank lines from removed directives
        while insert_idx < len(old_lines) and old_lines[insert_idx].strip() == "":
            insert_idx += 1
        old_lines.insert(insert_idx, "")
        old_lines.insert(insert_idx, block)
        new_content = "\n".join(line for line in old_lines if line is not None)

    BUILD_FILE.write_text(new_content)


def main() -> None:
    packages = find_local_packages()
    if not packages:
        print("No local packages found under packages/*/src/*/")
        return

    resolve_lines = generate_resolve_lines(packages)
    update_build_file(resolve_lines)

    print(f"Updated {BUILD_FILE.name} with resolve directives for: {', '.join(packages)}")
    for line in resolve_lines:
        print(f"  {line}")


if __name__ == "__main__":
    main()
