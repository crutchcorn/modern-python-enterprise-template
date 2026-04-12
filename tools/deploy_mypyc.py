"""Copy mypyc-compiled .so files from Bazel output into source packages.

This makes Python's import system pick up the compiled C extensions
instead of the pure-Python sources when running in production.

Usage: python tools/deploy_mypyc.py [--clean]
"""

import argparse
import glob
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAZEL_BIN = os.path.join(ROOT, ".bazel", "bin")
PACKAGES_DIR = os.path.join(ROOT, "packages")


def _is_extension(filename):
    """Check if a file is a compiled Python extension (.so or .pyd)."""
    return filename.endswith((".so", ".pyd"))


def find_mypyc_outputs():
    """Find all mypyc output directories under .bazel/bin/packages/."""
    pattern = os.path.join(BAZEL_BIN, "packages", "**", "*_mypyc")
    return glob.glob(pattern, recursive=True)


def deploy():
    """Copy compiled .so files into the corresponding source package dirs."""
    for mypyc_dir in find_mypyc_outputs():
        for root, _dirs, files in os.walk(mypyc_dir):
            for f in files:
                if _is_extension(f):
                    # Determine the package name from the directory structure
                    rel = os.path.relpath(root, mypyc_dir)  # e.g. "shared"
                    # Find matching source package
                    src_pkg = glob.glob(os.path.join(PACKAGES_DIR, "*", "src", rel))
                    if src_pkg:
                        dest = os.path.join(src_pkg[0], f)
                        shutil.copy2(os.path.join(root, f), dest)
                        print(f"  deployed: {os.path.relpath(dest, ROOT)}")


def clean():
    """Remove all deployed .so files from source packages."""
    for pkg_src in glob.glob(
        os.path.join(PACKAGES_DIR, "*", "src", "**"), recursive=True
    ):
        if _is_extension(os.path.basename(pkg_src)):
            os.remove(pkg_src)
            print(f"  removed: {os.path.relpath(pkg_src, ROOT)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--clean", action="store_true", help="Remove deployed .so files"
    )
    args = parser.parse_args()

    if args.clean:
        clean()
    else:
        deploy()


if __name__ == "__main__":
    main()
