from pathlib import Path
import re


def parse_model_definition(model_path: Path) -> dict[str, list[str]]:
    """PICTモデルファイルから
    因子順 + 各因子の水準定義順を取得する
    """
    model: dict[str, list[str]] = {}

    with model_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # サブモデルと制約条件の記述を除外し、モデルのみ後続の処理をする。
            if not re.search(r"^\s*([^:]+?)\s*:\s*(.+)$", line):
                continue

            factor, levels_part = line.split(":", 1)
            factor = factor.strip()

            levels = [
                level.strip() for level in levels_part.split(",") if level.strip()
            ]

            model[factor] = levels

    return model
