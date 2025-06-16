import sys
from pathlib import Path
import argparse
import os
from multiprocessing import Pool
import itertools

import scripts.runhelpers as rh
import scripts.bufferanalysis as ba


def run_analysis(workdir, config, dry_run, stats_only, disable_governor):
    pipeline_jobs = []
    config_out = config["out_dir"]
    actual_out = f"{workdir}/{config_out}"
    config_out_file = config["out_file"]
    actual_out_file = f"{workdir}/{config_out_file}"
    for strategy in config["strategy_mapping"].keys():
        pipeline_jobs += rh.prepare_runs(strategy, config["strategy_mapping"][strategy], actual_out, config["individual_num_runs"], config["debug"], workdir, config["eval-targets"], config["runtime"], config["use_python_modeling"], config["exp_name"] , stats_only)
    with Pool(config["num_cores"]) as p:
        p.starmap(rh.execute_command, zip(pipeline_jobs,itertools.repeat(config["debug"]), itertools.repeat(dry_run), itertools.repeat(disable_governor)))


def main(args):
    # this is scripts/experiment-01-01
    workdir = Path(os.path.dirname(os.path.realpath(__file__)))
    # the root of the eval
    basedir = workdir.parent.parent
    # the directory where the experiment runs
    experiment_dir = basedir / Path("01-dice-comparison/01-unit-tests/")
    config = rh.parse_config(experiment_dir)
    run_analysis(experiment_dir, config, args.dry_run, args.stats_only, args.disable_scaling_governor_check)
    ground_truth = ba.load_ground_truth(f"{experiment_dir}/ground_truth.yml")
    actual_out = os.path.join(experiment_dir,config["out_dir"])
    generated_configs = ba.find_all_generated_configs(actual_out)
    actual_out_file = os.path.join(experiment_dir,config["out_file"])
    ba.perform_analysis(generated_configs, ground_truth, actual_out_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog='Run-01-01',
            description='Docker wrapper to run experiment 01-01')
    parser.add_argument('-d', '--dry-run', action='store_true')
    parser.add_argument('-s', '--stats-only', action='store_true')
    parser.add_argument('-vm', '--disable-scaling-governor-check', action='store_true', help="If set, set AFL_SKIP_CPUFREQ=1 to disable checks for the correct scaling governor check")

    # command, num cores, starting core id, run synchronous
    args = parser.parse_args()
    main(args)
