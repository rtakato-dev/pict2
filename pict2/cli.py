"""CLI module for PICT2 wrapper tool.

This module provides command-line interface functionality for the PICT2 tool,
including argument parsing and main execution logic for generating combination
test cases from PICT model files.
"""

import argparse
from pathlib import Path
from typing import Any

from pict2.core.pict_runner import PictRunner
from pict2.mylib.normlize_pict_output import normalize_pict_output
from pict2.mylib.parse_model_definition import parse_model_definition
from pict2.mylib.sort_rows_by_model_order import sort_rows_by_model_order


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="pict2",
        description="PICT wrapper CLI tool",
    )

    parser.add_argument(
        "model",
        type=Path,
        help="PICT model file",
    )

    parser.add_argument(
        "-o",
        "--order",
        dest="order",
        help="Combination order (number or 'max')",
    )

    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        help="Output file path",
    )

    return parser.parse_args()


PICT_OPTION_TABLE: dict[str, dict[str, Any]] = {
    "order": {
        "has_value": True,
        "to_pict": lambda v: f"/o:{v}",
    },
    "random": {
        "has_value": "optional",
        "to_pict": lambda v: "/r" if v is None else f"/r:{v}",
    },
}


def main() -> None:
    args = parse_args()

    pict_options = []

    if args.order is None:
        pict_options.append("/o:max")

    for key, value in vars(args).items():
        if key == "file":
            output_path = value
        elif key in PICT_OPTION_TABLE:
            rule = PICT_OPTION_TABLE[key]
            if value is not None:
                pict_options.append(rule["to_pict"](value))

    runner = PictRunner()
    output = runner.run(
        model_path=args.model,
        pict_options=pict_options,
        output_path=None,
    )

    model_def = parse_model_definition(args.model)
    output = normalize_pict_output(output, model_def)
    output = sort_rows_by_model_order(
        rows=output.strip().splitlines()[1:],  # ヘッダを除く行
        factor_order=list(model_def.keys()),
        model_def=model_def,
    )
    output = output[0] + "\n" + "\n".join(output[1:])  # ヘッダを先頭に追加

    if output_path is not None:
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            f.write(output)
    else:
        print(output)
