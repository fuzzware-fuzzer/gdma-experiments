import sys
from pathlib import Path
import argparse
import os
from multiprocessing import Pool
import itertools

import scripts.runhelpers as rh


def main(args):
    workdir = Path(os.path.dirname(os.path.realpath(__file__)))
    basedir = workdir.parent.parent
    experiment_dir = basedir / Path("01-dice-comparison/02-real-firmware/")
    config = rh.parse_config(experiment_dir)
    pipeline_jobs = []
    config_out = config["out_dir"]
    actual_out = f"{experiment_dir}/{config_out}"
    config_out_file = config["out_file"]
    actual_out_file = f"{experiment_dir}/{config_out_file}"
    for strategy in config["strategy_mapping"].keys():
        pipeline_jobs += rh.prepare_runs(strategy, config["strategy_mapping"][strategy], actual_out, config["individual_num_runs"], config["debug"], experiment_dir, config["eval-targets"], config["runtime"], config["use_python_modeling"], config["exp_name"], args.stats_only)
    with Pool(config["num_cores"]) as p:
        p.starmap(rh.execute_command, zip(pipeline_jobs,itertools.repeat(config["debug"]), itertools.repeat(args.dry_run), itertools.repeat(args.disable_scaling_governor_check)))
    rh.parse_results(config["runtime_flexibility"], config["out_file"], os.path.join(workdir, config["out_dir"]), config["strategy_mapping"].keys())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Run-01-02',
        description='Docker wrapper to run experiment 01-02')
    parser.add_argument('-d', '--dry-run', action='store_true')
    parser.add_argument('-s', '--stats-only', action='store_true')
    parser.add_argument('-vm', '--disable-scaling-governor-check', action='store_true', help="If set, set AFL_SKIP_CPUFREQ=1 to disable checks for the correct scaling governor check")

    # command, num cores, starting core id, run synchronous
    args = parser.parse_args()
    main(args)
