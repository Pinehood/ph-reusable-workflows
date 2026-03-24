import json
import os
import sys


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(1)


def add_mask(value: str) -> None:
    if value:
        print(f"::add-mask::{value}")


def main() -> None:
    manual_args = os.environ.get("DOCKER_BUILD_ARGS", "").strip()
    mappings = os.environ.get("BW_DOCKER_BUILD_ARG_SECRETS", "")

    try:
        outputs = json.loads(os.environ.get("BW_OUTPUTS_JSON", "{}") or "{}")
    except json.JSONDecodeError as exc:
        fail(f"Invalid BW_OUTPUTS_JSON payload: {exc}")

    lines = []
    if manual_args:
        lines.append(manual_args)

    for raw_line in mappings.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if ">" not in line:
            fail(f"Invalid Bitwarden build arg mapping: {raw_line}")

        _, build_arg_name = [part.strip() for part in line.split(">", 1)]
        if not build_arg_name:
            fail(f"Missing build arg name in mapping: {raw_line}")

        secret_value = outputs.get(build_arg_name)
        if secret_value is None:
            fail(f"Bitwarden output '{build_arg_name}' was not returned.")

        build_arg = f"{build_arg_name}={secret_value}"
        add_mask(str(secret_value))
        add_mask(build_arg)
        lines.append(build_arg)

    github_output = os.environ.get("GITHUB_OUTPUT")
    if not github_output:
        fail("GITHUB_OUTPUT is not set.")

    with open(github_output, "a", encoding="utf-8") as output_file:
        output_file.write("build_args<<EOF\n")
        output_file.write("\n".join(lines))
        output_file.write("\nEOF\n")


if __name__ == "__main__":
    main()
