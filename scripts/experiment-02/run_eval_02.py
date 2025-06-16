import os
from pathlib import Path
import hashlib
import shutil
import sys
import subprocess
from multiprocessing import Pool
import itertools
import argparse

import scripts.runhelpers as rh


def warn(s):
    print(f"WARNING: {s}")


# walk IN_PATH, find all elfs, and record their relative path from IN_PATH
# returns a list of elf paths, ignoring the elfs in a `new/` directory
# as the parent directory is guaranteed to have an elf anyway and we want
# no duplicate directories
def collect_elf_dirs(in_path, eval_targets):
    result = set()
    for d, dirs, files in os.walk(in_path):
        if "output" in d or "deprecated" in d:
            continue
        # filter all paths that do not contain the targets from the config
        do_analysis=False
        for target in eval_targets:
            if target in d:
                do_analysis=True
        if not do_analysis:
            continue
        for file in files:
            if ".elf" in file:
                # if we are in a `new/` directory, skip it
                if os.path.basename(d) == "new":
                    # it can happen that we have a new folder and no parent elf
                    result.add(os.path.dirname(d))
                else:
                    result.add(d)
    return result


def main(args):
    global cfg
    workdir = Path(os.path.dirname(os.path.realpath(__file__)))
    basedir = workdir.parent.parent
    experiment_dir = basedir / Path("02-extended-test-suite/")
    cfg = rh.parse_config(experiment_dir) 
    config = cfg
    in_path = ""
    dirs_to_test = []
    target_dirs = []
    # the dirs with all targets
    for i in range(0,len(cfg["eval-targets"])):
        target_dir = os.path.join(experiment_dir,cfg["eval-targets"][i])
        target_dirs += target_dir
        # collect all dirs that we want to test
        dirs_to_test += collect_elf_dirs(target_dir, cfg["eval-targets"])
    pipeline_jobs = []
    config_out = config["out_dir"]
    actual_out = f"{experiment_dir}/{config_out}"
    config_out_file = config["out_file"]
    actual_out_file = f"{experiment_dir}/{config_out_file}"
    for strategy in cfg["strategy_mapping"].keys():
        pipeline_jobs += rh.prepare_runs(strategy, config["strategy_mapping"][strategy], actual_out, config["individual_num_runs"], config["debug"], experiment_dir, config["eval-targets"], config["runtime"], config["use_python_modeling"], config["exp_name"], args.stats_only)
    with Pool(cfg["num_cores"]) as p:
        p.starmap(rh.execute_command, zip(pipeline_jobs,itertools.repeat(config["debug"]), itertools.repeat(args.dry_run), itertools.repeat(args.disable_scaling_governor_check)))
    rh.parse_results(cfg["runtime_flexibility"], cfg["out_file"], os.path.join(experiment_dir, cfg["out_dir"]), cfg["strategy_mapping"].keys())

        
# this script assumes that prepare_eval has been run
# prepare_eval creates `new/` folders in the project dirs
# if the elf file it built differs from existing ones
#
# This script here generates configs for the new elfs
# and runs fuzzware on all the projects
#
# it expects to run inside docker with fuzzware installed
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='run_eval_02.py',
                    description='This is the script that runs eval 02. You most likely want to invoke the docker wrapper instead. \
                            If you want to invoke this script directly, make sure fuzzware is in the path and that you ran prepare_eval.py\
                            first, which is in `src/02-...`.')
    parser.add_argument('-u', '--update',
                    action='store_true', help="overwrite files in case of mismatch")
    parser.add_argument('-i', '--ignore',
                    action='store_true', help="ignore any file mismatches and take the files from the repo")
    parser.add_argument('-d', '--dry-run', action='store_true')
    parser.add_argument('-s', '--stats-only', action='store_true')
    parser.add_argument('-vm', '--disable-scaling-governor-check', action='store_true', help="If set, set AFL_SKIP_CPUFREQ=1 to disable checks for the correct scaling governor check")
    args = parser.parse_args()

    main(args)
