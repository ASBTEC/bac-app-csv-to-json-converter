import argparse
import os
import sys

from .reader import load_workbook, iter_rows
from .events import transform_event
from .exhibitors import transform_exhibitor
from .writer import write_json

_ROOT = os.path.join(os.path.dirname(__file__), "..")
DEFAULT_INPUT = os.path.join(_ROOT, "input", "Resumen_logistico.xlsx")
DEFAULT_OUTPUT = os.path.join(_ROOT, "output")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert BAC logistics XLSX to events.json and exhibitors.json."
    )
    parser.add_argument(
        "--input",
        default=DEFAULT_INPUT,
        help="Path to input .xlsx file (default: input/Resumen_logistico.xlsx)",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT,
        help="Directory for output JSON files (default: output/)",
    )
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    output_dir = os.path.abspath(args.output_dir)

    if not os.path.isfile(input_path):
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {input_path} …")
    wb = load_workbook(input_path)

    events = [transform_event(row) for row in iter_rows(wb["Events"], id_col="ID")]
    write_json(events, os.path.join(output_dir, "events.json"))

    exhibitors = [transform_exhibitor(row) for row in iter_rows(wb["Exhibitor"], id_col="ID exhibitor")]
    write_json(exhibitors, os.path.join(output_dir, "exhibitors.json"))

    print("Done.")


if __name__ == "__main__":
    main()
