# csv-to-json

Convert CSV to JSON from the terminal — zero-dependency Python CLI.

The header row becomes the object keys. Values are auto-typed:
integers and floats become numbers, `true`/`false` become booleans,
empty cells become `null`.

## Install

No dependencies — just Python 3.8+:

```sh
git clone https://github.com/heyzcx/csv-to-json.git
cd csv-to-json
```

## Usage

```sh
# Pretty-print a file
python csv_to_json.py example.csv --pretty

# One JSON object per line (default, pipe-friendly)
python csv_to_json.py example.csv

# Read from stdin, write to a file as a bare JSON array
cat data.csv | python csv_to_json.py -o out.json --array

# Keep every value a string (no type inference)
python csv_to_json.py example.csv --no-infer
```

## Options

| Flag | Description |
| --- | --- |
| `input` | CSV file to read (default: stdin) |
| `-o, --output` | Write JSON to a file instead of stdout |
| `--indent N` | Indent JSON by N spaces (default: compact) |
| `--pretty` | Shortcut for `--indent 2` |
| `--array` | Emit a bare JSON array instead of one object per line |
| `--no-infer` | Keep all values as strings |

## Example

`example.csv`:

```csv
name,age,city,subscribed
Alice,30,New York,true
Bob,25,San Francisco,false
```

```sh
$ python csv_to_json.py example.csv --pretty
[
  {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "subscribed": true
  },
  {
    "name": "Bob",
    "age": 25,
    "city": "San Francisco",
    "subscribed": false
  }
]
```

## License

MIT
