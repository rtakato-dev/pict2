def sort_rows_by_model_order(rows, factor_order, model_def):
    level_index = {
        factor: {level: i for i, level in enumerate(levels)}
        for factor, levels in model_def.items()
    }

    split_rows = [row.split("\t") for row in rows]

    def sort_key(row):
        return tuple(
            level_index[factor][value] for factor, value in zip(factor_order, row)
        )

    sorted_rows = sorted(split_rows, key=sort_key)

    return ["\t".join(row) for row in [factor_order] + sorted_rows]
