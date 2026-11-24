#!/usr/bin/env python3
"""Convert CSV to JSON from the terminal — zero-dependency Python CLI.

Usage:
    python csv_to_json.py input.csv [-o output.json] [--indent 2]
    cat data.csv | python csv_to_json.py
    python csv_to_json.py input.csv --array   # emit a bare JSON array
    python csv_to_json.py input.csv --pretty  # pretty-print with indent 2

Rows become objects keyed by the header row. Values are auto-typed:
integers and floats are parsed as numbers, "true"/"false" as booleans,
empty cells become null. Use --no-infer to keep every value a string.
"""
import argparse
import csv
import json
import sys


def infer(value):
    """Best-effort typing for a CSV cell."""
    if value == "":
        return None
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def convert(rows, infer_types=True):
    """Turn an iterable of CSV rows (first row = header) into a list of dicts."""
    rows = iter(rows)
    try:
        header = next(rows)
    except StopIteration:
        return []
    header = [h.strip() for h in header]
    out = []
    for row in rows:
        if not row or all(cell.strip() == "" for cell in row):
            continue
        record = {}
        for i, key in enumerate(header):
            cell = row[i] if i < len(row) else ""
            record[key] = infer(cell) if infer_types else cell
        out.append(record)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert CSV to JSON (header row becomes object keys).")
    parser.add_argument("input", nargs="?", help="CSV file (default: stdin)")
    parser.add_argument("-o", "--output", help="Write JSON to file (default: stdout)")
    parser.add_argument("--indent", type=int, default=None,
                        help="Indent JSON by N spaces (default: compact)")
    parser.add_argument("--pretty", action="store_true",
                        help="Shortcut for --indent 2")
    parser.add_argument("--array", action="store_true",
                        help="Emit a bare JSON array instead of one object per line")
    parser.add_argument("--no-infer", action="store_true",
                        help="Keep all values as strings")
    args = parser.parse_args(argv)

    source = open(args.input, newline="", encoding="utf-8") if args.input else sys.stdin
    try:
        records = convert(csv.reader(source), infer_types=not args.no_infer)
    finally:
        if args.input:
            source.close()

    indent = 2 if args.pretty else args.indent
    if args.array or indent is not None:
        text = json.dumps(records, indent=indent, ensure_ascii=False)
    else:
        text = "\n".join(json.dumps(r, ensure_ascii=False) for r in records)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
