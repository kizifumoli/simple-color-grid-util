#!/usr/bin/env python3

from lib import color_grid

import argparse
import sys
import json

from pathlib import Path
from datetime import datetime

"""Sample Json:
{
  "n_rows": 2,
  "n_cols": 3,
  "data": [
    "ffffff",
    "ffffff",
    "ffffff",
    "ffffff",
    "ffffff",
    "000000"
  ]
}

"""

def create_color_grid_fn(json_input: Path, output_directory: Path):
    with open(json_input) as color_fd:
        color_json = json.load(color_fd)
        cgrid = color_grid.ColorGrid.from_json(color_json)

        now = datetime.now().strftime("%Y_%m_%d_%H:%M:%S")

        stem = "color_grid_generated_at_" + now + ".png"
        output_file = output_directory / stem
        cgrid.to_image(output_file)
        print(f"Saved image to {output_file}")


def create_argparser() -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser()
    subparsers = argparser.add_subparsers()

    color_grid_cmd = subparsers.add_parser("create-color-grid")
    color_grid_cmd.add_argument(
        "--json-input", help="Filepath to json file containing colors",
        required=True
    )
    color_grid_cmd.add_argument(
        "--output-directory", type=Path, help="Output directory for the color grid image",
        default="/tmp/"
    )

    color_grid_cmd.set_defaults(func=lambda args: create_color_grid_fn(args.json_input, args.output_directory))
    return argparser

def main():
    argparser = create_argparser()
    if (len(sys.argv) <= 1):
        argparser.print_help()
        exit(1)

    args = argparser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
