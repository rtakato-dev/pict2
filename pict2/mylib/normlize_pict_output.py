def normalize_pict_output(
    pict_output: str,
    model_def: dict[str, list[str]],
    delimiter: str = "\t",
) -> str:
    lines = pict_output.strip().splitlines()
    if not lines:
        return pict_output

    header = lines[0].split(delimiter)
    rows = [line.split(delimiter) for line in lines[1:]]

    # 出力ヘッダ -> index
    header_index = {name: i for i, name in enumerate(header)}

    # モデル定義順
    factor_order = list(model_def.keys())

    # 並び替えインデックス
    try:
        indices = [header_index[f] for f in factor_order]
    except KeyError as e:
        raise RuntimeError(f"Factor not found in PICT output: {e}")

    # 正規化済み出力
    output_lines: list[str] = []
    output_lines.append(delimiter.join(factor_order))

    for row in rows:
        new_row: list[str] = []

        for factor, idx in zip(factor_order, indices):
            value = row[idx]
            allowed_levels = model_def[factor]

            if value not in allowed_levels:
                raise RuntimeError(
                    f"Invalid level '{value}' for factor '{factor}'. "
                    f"Allowed: {allowed_levels}",
                )

            # 水準はモデル定義の文字列表現をそのまま使う
            new_row.append(value)

        output_lines.append(delimiter.join(new_row))

    return "\n".join(output_lines)
