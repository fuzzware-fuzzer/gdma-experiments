import os
import hashlib
import shutil
import sys
import subprocess
from multiprocessing import Pool
import itertools
import argparse
from pathlib import Path

import scripts.runhelpers as rh


def main(args):
    workdir = Path(os.path.dirname(os.path.realpath(__file__)))
    basedir = workdir.parent.parent
    experiment_dir = basedir / Path("04-finding-new-bugs/")
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

        
# This script here generates configs for the new elfs
# and runs fuzzware on all the projects
#
# it expects to run inside docker with fuzzware installed
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='run_eval_04.py',
                    description='This is the script that runs eval 04. You most likely want to invoke the docker wrapper instead. \
                            If you want to invoke this script directly, make sure fuzzware is in the path.')
    parser.add_argument('-d', '--dry-run', action='store_true')
    parser.add_argument('-s', '--stats-only', action='store_true')
    parser.add_argument('-vm', '--disable-scaling-governor-check', action='store_true', help="If set, set AFL_SKIP_CPUFREQ=1 to disable checks for the correct scaling governor check")

    args = parser.parse_args()
    main(args)
