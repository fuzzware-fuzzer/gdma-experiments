#!/usr/bin/env python3

import argparse

from pathlib import Path

try:
    from fuzzware_pipeline import naming_conventions as nc
except ImportError as e:
    print("[ERROR] Could not import from fuzzware. Please run in docker or venv...")
    exit(1)

from diffing import add_modeldiff_parsing
from modeling import add_modelgen_parsing
from groundtruthdiffing import add_groundtruth_diff_parsing
from oob_check import add_oob_check_parsing

DEFAULT_REVISION_NAME = "regen"
def setup_common_arg_parser():
    """
    Setup the args for the argparser
    """
    common_parser = argparse.ArgumentParser()
    common_parser.add_argument('root', nargs="+", type=Path, help = "Root directory to scan for project directories in.")
    common_parser.add_argument('--name', type=str, default=DEFAULT_REVISION_NAME, help=f"Name of this re-generation. Results per project will be stored in {nc.PIPELINE_DIRNAME_DMA_SNIPPETS}_<revision_name>. Defaults to {DEFAULT_REVISION_NAME}.")
    common_parser.add_argument('-j', '--num-cores', default = 1, type = int, help = "Number of cores to use for modeling")
    common_parser.add_argument('-v', '--verbose', action="store_true", default=False, help="Print verbose output.")

    return common_parser

def main():
    parser = argparse.ArgumentParser(description="DMA model generation and diffing")
    main_parsers = parser.add_subparsers(required=True, title="DMA Actions", help='List of DMA actions')
    def do_help(args):
        parser.parse_args(['-h'])
    parser.set_defaults(func=do_help)

    common_parser = setup_common_arg_parser()
    add_modelgen_parsing(common_parser, main_parsers)
    add_modeldiff_parsing(common_parser, main_parsers)
    add_groundtruth_diff_parsing(common_parser, main_parsers)
    add_oob_check_parsing(common_parser, main_parsers)

    args = parser.parse_args()

    if type(args.root) == list:
        for root_dir in args.root:
            if not root_dir.exists():
                print(f"[ERROR] Passed non-existant root directory '{root_dir}'. Exiting...")
                exit(1)

    args.func(args)

if __name__ == "__main__":
    main()
