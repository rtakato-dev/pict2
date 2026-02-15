import csv


def unique_preserve_order(seq):
    seen = set()
    result = []
    for x in seq:
        if x not in seen:
            seen.add(x)
            result.append(x)
    return result


def convert_to_decision_tab(tsv_text: str):
    reader = csv.reader(tsv_text.splitlines(), delimiter="\t")
    rows = list(reader)

    header = rows[0]
    test_cases = rows[1:]

    decision_rows = []

    for col_idx, header in enumerate(header):
        column_values = [
            case[col_idx]
            for case in test_cases
            if col_idx < len(case) and case[col_idx] != ""
        ]
        condition_values = unique_preserve_order(column_values)

        for cond in condition_values:
            row = [header, cond, ""]

            for case in test_cases:
                cell = case[col_idx] if col_idx < len(case) else ""
                row.append("○" if cell == cond else "-")

            decision_rows.append(row)

    return "\n".join("\t".join(row) for row in decision_rows)
