# myproject/cli.py
import argparse
from pathlib import Path

from pict2.mylib.mylib import PictRunner


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
        dest="order",
        help="Combination order (number or 'max')",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    pict_options = []

    # -o の扱い（最小実装）
    if args.order is not None:
        pict_options.extend(["/o:" + args.order])

    if args.order is None:
        pict_options.extend(["/o:max"])

    runner = PictRunner()
    output = runner.run(
        model_path=args.model,
        pict_options=pict_options,
    )

    print(output)
