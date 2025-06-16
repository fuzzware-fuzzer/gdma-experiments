from fuzzware_harness.util import load_config_deep, parse_address_value, parse_symbols
from fuzzware_pipeline import do_gentraces
from fuzzware_pipeline.util import find_proj
from fuzzware_pipeline import naming_conventions as nc
from pathlib import Path

import argparse
import yaml

def add_oob_check_parsing(common_parser, sub_parsers):
    parser = sub_parsers.add_parser(
        "oob-check", help="Check for out of bounds DMA writes", add_help=False, parents=[common_parser]
    )
    parser.set_defaults(func=oob_check_main)

    parser.add_argument("--crashes", action="store_true", default=False, help="Check crashes instead of queue inputs")
    parser.add_argument("--targets-root", type=Path, help="Overwrite the root targets directory")
    parser.add_argument("--print-all", action="store_true", default=False, help="Print all OOB accesses, default is to only print the first per project")
    parser.add_argument("--skip-gentraces", action="store_true", default=False, help="Skip generating traces, usefull if all traces were already generated")

def trace_oob_check(trace, buffer_ranges, print_all):
    log = ""
    for line in trace.splitlines():
        dma_idx, pc, lr, direction, input_idx, size, addr, value = line.split(" ")
        addr = int(addr.strip(":"), 16)
        if not any(addr in r for r in buffer_ranges):
            log += f"OOB dma write at {addr:#x} pc: {pc} lr: {lr}\n"
            if not print_all:
                return log
    return log

def oob_check_main(args):
    projdirs = []
    for root_dir in args.root:
        projdirs.extend(find_proj.find_projdirs(root_dir))

    if not projdirs:
        print("Found no project directories. Nothing to do...")
        exit(1)

    print(f"Got {len(projdirs)} project directories")

    proj_logs = {}
    for projdir in projdirs:
        print(f"Processing {projdir}")
        proj_path = Path(projdir)
        # assume folder layout:
        # project: xxx/output/*/target_name/run_id/fuzzware-project
        # configs: xxx/targets/target_name/config_generic_dma_manual.yml
        target_name = proj_path.parent.parent.name
        if args.targets_root is None:
            config_path = proj_path.parent.parent.parent.parent.parent.joinpath("targets", target_name, "config_generic_dma_manual.yml")
        else:
            config_path = args.targets_root.joinpath(target_name, "config_generic_dma_manual.yml")

        assert config_path.exists()

        # collect all valid buffer ranges from the dma config
        config = load_config_deep(config_path)
        symbols, _ = parse_symbols(config)
        peripheral_config = config["peripherals"].popitem()[1]

        buffer_ranges = []
        for address_value, known_size in peripheral_config["known_sizes"].items():
            addr = parse_address_value(symbols, address_value)
            min = addr
            max = addr + known_size["max"]
            buffer_ranges.append(range(min, max))

        if not args.skip_gentraces:
            tracegen_args = argparse.Namespace(
                dryrun=False,
                trace_types=["dma"],
                fuzzers="1",
                main_dirs="all",
                projdir=projdir,
                all=False,
                tracedir_postfix=None,
                verbose=False,
                crashes=args.crashes,
                num_instances=args.num_cores,
                force_slow_tracing=False,
                force_process_per_input=False,
            )
            do_gentraces(tracegen_args, None)

        stop = False
        proj_log = ""
        # iterate through all input traces and collect logs from the checker
        for main_dir in nc.main_dirs_for_proj(projdir):
            for input_path in nc.input_paths_for_main_dir(main_dir, crashes=args.crashes):
                trace_path = nc.trace_for_input_path(input_path, nc.PREFIX_DMA_TRACE)
                trace = open(trace_path).read()
                trace_log = trace_oob_check(trace, buffer_ranges, args.print_all)
                proj_log += trace_log
                if trace_log and not args.print_all:
                    stop = True
                    break
            if stop:
                break

        proj_logs[projdir] = proj_log

    # print the logs in the end or else they get lost in the gentraces output
    for projdir, proj_log in proj_logs.items():
        if proj_log:
            print(projdir)
            print(proj_log)
