"""Bazel rule for compiling Python packages with mypyc.

Usage in BUILD.bazel:

    load("//tools:mypyc.bzl", "mypyc_library")

    mypyc_library(
        name = "shared_mypyc",
        package_name = "shared",
        srcs = ["__init__.py"],
    )
"""

def _mypyc_library_impl(ctx):
    # Output is a directory tree: <name>/<package_name>/<compiled .so files>
    compiled_dir = ctx.actions.declare_directory(ctx.attr.name)

    # Build the argument list for the compile script
    src_args = " ".join([src.path for src in ctx.files.srcs])
    script = ctx.file._compiler_script

    # Use `uv run python` to invoke the system Python (free-threaded),
    # so the compiled .so matches the production runtime ABI.
    # --with flags ensure mypy/setuptools are available in the ephemeral env.
    ctx.actions.run_shell(
        command = "uv run --with mypy --with setuptools python {script} --output-dir {out} --package-name {pkg} {srcs}".format(
            script = script.path,
            out = compiled_dir.path,
            pkg = ctx.attr.package_name,
            srcs = src_args,
        ),
        inputs = ctx.files.srcs + [script],
        outputs = [compiled_dir],
        mnemonic = "MypycCompile",
        progress_message = "Compiling %{label} with mypyc",
        # mypyc invokes the system C compiler, which needs PATH and other env vars
        use_default_shell_env = True,
        execution_requirements = {"no-sandbox": "1"},
    )

    return [DefaultInfo(
        files = depset([compiled_dir]),
    )]

mypyc_library = rule(
    implementation = _mypyc_library_impl,
    attrs = {
        "srcs": attr.label_list(
            allow_files = [".py"],
            mandatory = True,
            doc = "Python source files to compile with mypyc.",
        ),
        "package_name": attr.string(
            mandatory = True,
            doc = "The Python package name (used for directory structure).",
        ),
        "_compiler_script": attr.label(
            default = "//tools:mypyc_compile.py",
            allow_single_file = True,
        ),
    },
    doc = "Compile Python sources to native C extensions using mypyc.",
)
