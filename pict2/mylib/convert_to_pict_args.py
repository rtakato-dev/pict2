"""Convert UNIX-style CLI options to PICT native format."""
from typing import list

PICT_OPTION_TABLE: dict[str, dict[str, Any]] = {
    "-o": {
        "has_value": True,
        "to_pict": lambda v: f"/o:{v}",
    },
    "-r": {
        "has_value": "optional",
        "to_pict": lambda v: "/r" if v is None else f"/r:{v}",
    },
}

def convert_to_pict_args(options: list[str]) -> list[str]:
    """UNIX風CLIオプションを PICT ネイティブ形式に変換する"""
    pict_args: list[str] = []
    i = 0

    while i < len(options):
        opt = options[i]

        if opt not in PICT_OPTION_TABLE:
            raise ValueError(f"Unsupported option: {opt}")

        rule = PICT_OPTION_TABLE[opt]
        has_value = rule["has_value"]

        # 値を取らない
        if has_value is False:
            pict_args.append(rule["to_pict"](None))
            i += 1
            continue

        # 必ず値を取る
        if has_value is True:
            if i + 1 >= len(options):
                raise ValueError(f"Option requires a value: {opt}")
            value = options[i + 1]
            pict_args.append(rule["to_pict"](value))
            i += 2
            continue

        # 値が任意（-r / -r 42）
        if has_value == "optional":
            # 次がオプションなら値なしと判断
            if i + 1 >= len(options) or options[i + 1].startswith("-"):
                pict_args.append(rule["to_pict"](None))
                i += 1
            else:
                value = options[i + 1]
                pict_args.append(rule["to_pict"](value))
                i += 2
            continue

        raise RuntimeError(f"Invalid option rule: {opt}")

    return pict_args
