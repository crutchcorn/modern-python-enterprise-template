"""Export the FastAPI OpenAPI spec to a JSON file."""

import argparse
import json
import sys

from main import app


def export_openapi(output: str | None = None) -> None:
    spec = app.openapi()
    text = json.dumps(spec, indent=2)

    if output:
        with open(output, "w") as f:
            f.write(text)
    else:
        sys.stdout.write(text)
        sys.stdout.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export FastAPI OpenAPI spec")
    parser.add_argument(
        "-o", "--output", help="Output file path (default: stdout)", default=None
    )
    args = parser.parse_args()
    export_openapi(args.output)
