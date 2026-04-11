"""Compile Python source files with mypyc.

Usage: mypyc_compile --output-dir <dir> --package-name <name> <src1.py> [src2.py ...]

Creates <dir>/<package_name>/ containing the compiled .so extension module(s).
"""

import argparse
import os
import shutil
import sys
import sysconfig
import tempfile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--package-name", required=True)
    parser.add_argument("srcs", nargs="+")
    args = parser.parse_args()

    ext_suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"

    # Resolve output-dir to absolute before changing cwd
    output_dir = os.path.abspath(args.output_dir)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Recreate package directory structure so mypyc sees a proper package
        pkg_dir = os.path.join(tmpdir, args.package_name)
        os.makedirs(pkg_dir)

        for src in args.srcs:
            shutil.copy2(src, os.path.join(pkg_dir, os.path.basename(src)))

        # Change to tmpdir so setuptools build_ext --inplace writes .so here
        orig_cwd = os.getcwd()
        os.chdir(tmpdir)

        try:
            # Use mypyc's Python API directly (avoids subprocess + PATH issues)
            from mypyc.build import mypycify

            src_paths = [
                os.path.join(pkg_dir, os.path.basename(s)) for s in args.srcs
            ]
            ext_modules = mypycify(src_paths)

            if not ext_modules:
                print("mypyc: no extension modules produced", file=sys.stderr)
                sys.exit(1)

            # Build the extensions using setuptools
            from setuptools import Distribution

            dist = Distribution({"ext_modules": ext_modules})
            dist.package_dir = {}
            cmd = dist.get_command_obj("build_ext")
            cmd.inplace = True
            cmd.ensure_finalized()
            cmd.run()
        finally:
            os.chdir(orig_cwd)

        # Search the entire tmpdir for compiled .so files and copy them out
        out_pkg = os.path.join(output_dir, args.package_name)
        os.makedirs(out_pkg, exist_ok=True)

        for root, _dirs, files in os.walk(tmpdir):
            for f in files:
                if f.endswith(ext_suffix):
                    # Rename <package>.cpython-XXX.so -> __init__.cpython-XXX.so
                    # so Python loads it as the package's __init__ module
                    dest_name = f
                    pkg_prefix = args.package_name + "."
                    if f.startswith(pkg_prefix):
                        dest_name = "__init__." + f[len(pkg_prefix):]
                    shutil.copy2(os.path.join(root, f), os.path.join(out_pkg, dest_name))
                    print(f"  compiled: {args.package_name}/{dest_name}")


if __name__ == "__main__":
    main()
