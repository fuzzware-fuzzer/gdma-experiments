import importlib
import time
import argparse
from datetime import timedelta, datetime
import subprocess
import yaml
import os
from pathlib import Path
import multiprocessing
import json

def pp(d):
    print(json.dumps(d, sort_keys=True, indent=4))


# config is an experiment config, experiment is a path to a ".config.yml"
def update_experiment_config(config, experiment, dry_run):
    experiment_config = {}
    with open(experiment) as outfile:
        experiment_config = yaml.safe_load(outfile)
    experiment_config["num_cores"] = config["cores-per-experiment"]
    experiment_config["runtime"] = config["fuzzing-time"]
    experiment_config["individual_num_runs"] = config["runs-per-firmware"]
    # Write YAML file
    if dry_run:
        print(f"Dumping config for experiment {experiment}:")
        pp(experiment_config)
        print()
    else:
        with open(experiment, 'w', encoding='utf8') as outfile:
            yaml.dump(experiment_config, outfile, allow_unicode=True)


# new_config is the overarching config for the complete run
def update_configs(new_config, basedir, dry_run):
    targets = new_config["experiments"]
    print(targets)
    for target in targets:
        target = f"{basedir}/{target}.config.yml"
        update_experiment_config(new_config, target, dry_run)


def load_config():
    # config is always next to the eval script
    file_path = Path(os.path.realpath(__file__)).parent
    with open(f"{file_path}/.experiments-config.yml") as stream:
        return yaml.safe_load(stream)


def run_experiments(config, basedir, args):
    targets = sorted(config["experiments"])
    for target in targets:
        if target == "01-dice-comparison/01-unit-tests/":
            run_experiment_1_1(f"{basedir}/{target}", config, args)
        if target == "01-dice-comparison/02-real-firmware/":
            run_experiment_1_2(f"{basedir}/{target}", config, args)
        if target == "02-extended-test-suite/":
            run_experiment_2(f"{basedir}/{target}", config, args)
        if target == "03-coverage-experiments/":
            run_experiment_3(f"{basedir}/{target}", config, args)
        if target == "04-finding-new-bugs/":
            run_experiment_4(f"{basedir}/{target}", config, args)
        if target == "05-false-positive/":
            run_experiment_5(f"{basedir}/{target}", config, args)


# we have one function for each experiment to estimate runtime easier
def run_experiment_1_1(directory, config, args):
    mod = importlib.import_module("experiment-01-01.docker_eval_wrapper")
    mod.main(args)


def run_experiment_1_2(directory, config, args):
    mod = importlib.import_module("experiment-01-02.docker_eval_wrapper")
    mod.main(args)

def run_experiment_2(directory, config, args):
    mod = importlib.import_module("experiment-02.docker_eval_02_wrapper")
    mod.main(args)

def run_experiment_3(directory, config, args):
    mod = importlib.import_module("experiment-03.docker_eval_wrapper")
    mod.main(args)

def run_experiment_4(directory, config, args):
    mod = importlib.import_module("experiment-04.docker_eval_wrapper")
    mod.main(args)

def run_experiment_5(directory, config, args):
    mod = importlib.import_module("experiment-05.docker_eval_wrapper")
    mod.main(args)


def check_limits(disable_governor_check):
    # inotify checks
    inst_fp = open("/proc/sys/fs/inotify/max_user_instances","r")
    inst_num = int(inst_fp.read().strip())
    inst_fp.close()
    if inst_num < 512:
        print("Please increase the inotify max user instances to at least 512\necho 512 > /proc/sys/fs/inotify/max_user_instances")
        sys.exit(-1)
    watch_fp = open("/proc/sys/fs/inotify/max_user_watches","r")
    watch_num = int(watch_fp.read().strip())
    watch_fp.close()
    if watch_num < 524288:
        print("Please increase the inotify max user watches to at least 524288\necho 524288 > /proc/sys/fs/inotify/max_user_watches")
        sys.exit(-1)
    # afl checks
    core_pattern_fp = open("/proc/sys/kernel/core_pattern")
    core_pattern = core_pattern_fp.read().strip()
    core_pattern_fp.close()
    if core_pattern != "core":
        print("Please set core_pattern to core: echo core >/proc/sys/kernel/core_pattern")
        sys.exit(-1)
    if not disable_governor_check:
        num_cores = multiprocessing.cpu_count()
        for i in range(0,num_cores):
            fp = open(f"/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_governor")
            mode = fp.read().strip()
            if mode != "performance":
                print("Please set scaling governor mode to performance: cd /sys/devices/system/cpu; echo performance | tee cpu*/cpufreq/scaling_governor")
                sys.exit(-1)


def main(args):
    file_path = Path(os.path.realpath(__file__)).parent.parent
    # check if inotify limits and afl requirements are setup properly
    check_limits(args.disable_scaling_governor_check)
    config = load_config()
    if args.regen_configs: 
        update_configs(config, file_path, args.dry_run)
    run_experiments(config, file_path, args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Experiments runner',
                    description='This script runs all experiments from the paper in order. Checkout ".experiments-config.yml" for configuration options for the experiments.')
    parser.add_argument('-r', '--regen-configs',
                    action='store_true', help="If set, propagate \".experiments-config.yml\" parameters to all experiments. Otherwise use the defaults from the experiment. ")
    parser.add_argument('-d', '--dry-run', action='store_true', help="If set, print executed commands instead of running them")
    parser.add_argument('-s', '--stats-only', action='store_true', help="Only execute genstats and skip pipeline")
    parser.add_argument('-vm', '--disable-scaling-governor-check', action='store_true', help="If set, set AFL_SKIP_CPUFREQ=1 to disable checks for the correct scaling governor check")


    args = parser.parse_args()
    main(args)
