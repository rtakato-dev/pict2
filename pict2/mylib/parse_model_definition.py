from pathlib import Path
from typing import Dict, List


def parse_model_definition(model_path: Path) -> Dict[str, List[str]]:
    """
    PICTモデルファイルから
    因子順 + 各因子の水準定義順を取得する
    """
    model: Dict[str, List[str]] = {}

    with model_path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                continue

            factor, levels_part = line.split(":", 1)
            factor = factor.strip()

            levels = [
                level.strip() for level in levels_part.split(",") if level.strip()
            ]

            model[factor] = levels

    return model
