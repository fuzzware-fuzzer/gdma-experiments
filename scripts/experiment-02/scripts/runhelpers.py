import sys
from pathlib import Path
import os
import shutil
from multiprocessing import Pool
import yaml
import itertools

# path to fuzzware-project folder
# e.g. /home/user/fuzzware/targets/dice-samples/manual-generic-dma/GPS-Receiver/GPS-Receiver-1/fuzzware-project
def prepare_metadata(path, strategies):
    # something like /home/user/fuzzware/targets/dice-samples/manual-generic-dma/GPS-Receiver/GPS-Receiver-1
    firmware_run_name_dir = os.path.split(path)[0]
    # something like
    # /home/user/fuzzware/targets/dice-samples/manual-generic-dma/GPS-Receiver/, GPS-Receiver-1
    firmware_top_dir, firmware_run_name = os.path.split(firmware_run_name_dir)
    # the run index, 1 in this example
    run_index = firmware_run_name[-1]
    # strategy and firmware name
    # /home/user/fuzzware/targets/dice-samples/manual-generic-dma/, GPS-Receiver
    _, firmware_name = os.path.split(firmware_top_dir)
    # finally, the strategy name
    strategy_name = None
    for strategy in strategies:
        if strategy in path:
            strategy_name = strategy
    assert(strategy_name)
    # the info that we need for the table later
    metadata = (strategy_name, firmware_name, run_index)
    return metadata

# returns true if we differ at most RUNTIME_FLEXIBILITY from planned runtime
def verify_runtime(path, runtime_flexibility):
    runtime_path = os.path.join(path,"logs","runtime.txt")
    correct_runtime = False
    with open(runtime_path,"r") as f:
        lines = f.readlines()
        # layout: <name> : value
        planned_runtime = int(lines[0].strip().split(":")[1].strip())
        start_epoch = int(lines[1].strip().split(":")[1].strip())
        end_epoch = int(lines[2].strip().split(":")[1].strip())
        actual_runtime = end_epoch - start_epoch
        runtime_delta = abs(actual_runtime - planned_runtime)
        if runtime_delta <= runtime_flexibility:
            correct_runtime = True
    return correct_runtime

# get block coverage for run and return it
def get_block_coverage(path):
    block_coverage_path = os.path.join(path, "stats","covered_bbs_by_second_into_experiment.csv")
    coverage = 0
    with open(block_coverage_path,"r") as f:
        lines = f.readlines()
        last_coverage_line = lines[-1].strip()
        # format: <seconds into experiments> <#covered blocks>
        coverage = (last_coverage_line.split("\t"))[1]
    return coverage

# extract milestones and if they are covered
# this also needs the metadata, as Guitar-Pedal has a special verification script
def get_milestone_coverage(path, metadata):
    milestone_coverage_path = os.path.join(path,"stats","milestone_discovery_timings.csv")
    milestone_coverage = {}
    with open(milestone_coverage_path,"r") as f:
        # flexible number of milestones
        for line in f.readlines():
            line = line.strip()
            milestone_addr, cov = line.split("\t")
            milestone_coverage[milestone_addr] = cov
    return milestone_coverage

# add results to the global dict
def add_to_results(metadata, correct_runtime, block_cov, milestone_cov, results):
    strategy_name, firmware_name, run_index = metadata
    # does the strategy already exist from a previous eval?
    if not strategy_name in results.keys():
        results[strategy_name]={}
    # did we analyze other runs of the same firmware already?
    if not firmware_name in results[strategy_name].keys():
        results[strategy_name][firmware_name] = {}
    result = {"runtime": correct_runtime, "blocks_covered": block_cov, "milestones_covered":milestone_cov}
    run_str = "run-" + str(run_index)
    results[strategy_name][firmware_name][run_str] = result

# path to fuzzware-project folder
# e.g. /home/user/fuzzware/targets/dice-samples/manual-generic-dma/GPS-Receiver/GPS-Receiver-1/fuzzware-project
def retrieve_stats(path, runtime_flexibility, results, strategies):
    # (strategy_name, firmware_name, run_index)
    # manual-generic-dma, GPS-Receover, 1
    metadata = prepare_metadata(path, strategies)
    # now we need to actually retrieve the stats
    # this is done in 3 steps:
    # 1. retrieve runtime duration to verify it did run about 24 hours
    #   we look at the runtime.txt in logs/ for that
    correct_runtime = True
    try:
        correct_runtime = verify_runtime(path, runtime_flexibility)
    except Exception:
        # sometimes the file is not created, we treat it as wrong runtime
        correct_runtime = False
    if not correct_runtime:
        print(f"Warning: project at {path} did not stay within runtime boundaries!")
    # 2. retrieve coverage
    # to be found in stats/covered_bbs_by_second_into_experiment.csv

    try:
        block_cov = coverage = get_block_coverage(path)
        # 3. retrieve milestone coverage
        milestone_cov = get_milestone_coverage(path, metadata)
        # add it all to the results dict
        add_to_results(metadata, correct_runtime, block_cov, milestone_cov, results)
    except Exception as e:
        print(e)
        pass

# the top-level function for analyzing the results
def parse_results(runtime_flexibility, out_file, in_path, strategies):
    # get all directories that contain "config.yml" and are not in the out_dir
    target_dirs = []
    for subdir, dirs, files in os.walk(in_path):
        if os.path.basename(subdir) == "fuzzware-project":
            target_dirs.append(subdir)
    results = {}
    for d in target_dirs:
        retrieve_stats(d, runtime_flexibility, results, strategies)
    # and dump it as yaml
    yaml_results = yaml.dump(results, sort_keys = False)
    target_dir = Path(in_path).parent
    target_dir = os.path.join(target_dir,out_file)
    with open(target_dir,"w") as f:
        f.write(yaml_results)

# glorified os.system wrapper
def execute_command(command, debug, dry_run, disable_governor_check):
    if disable_governor_check:
        print("Disabling governor check")
        os.putenv("AFL_SKIP_CPUFREQ","1")
    if dry_run:
        print(command)
    else:
        os.system(command)

# craft the fuzzware command and add it to the global queue
# out_path is the path in `output/`, `in_path` the path where to take the config from
def add_fuzzware_commands(strategy, out_path, in_path, strategy_config, runtime, use_python_modeling, stats_only):
    out_proj_path = os.path.join(out_path,"fuzzware-project")
    config_path = os.path.join(in_path,strategy_config)
    milestone_bb_path = os.path.join(in_path,"milestone_bbs.txt")
    out_path_tmp = os.path.dirname(out_path)
    dma_flag = ""
    if strategy == "automatic-generic-dma":
        if use_python_modeling:
            dma_flag = "--dma-in-python"
        else:
            dma_flag += "--dma"
    from random import random
    MAX_SLEEP_SEC = 30
    modeling = ""
    command = ""
    if not stats_only:
        command_run = f"sleep {round(random()*MAX_SLEEP_SEC,4)} && fuzzware pipeline {dma_flag} -c {config_path} --run-for {runtime} -o {out_proj_path};"
        command += command_run
    command_stats = f"sleep {round(random()*MAX_SLEEP_SEC,4)} && fuzzware genstats -p {out_proj_path} --milestone-bb-file {milestone_bb_path} --i-am-aware-i-am-overcounting-translation-blocks-so-force-skip-valid-bb-file"
    command += command_stats
    return command


# create the output structure of the evaluation for a given strategy
# (nodma, reference,...) target (path to directory with all relevant configs)
# and target name (the name under which you want to run the evaluation firmware)
# also adds the fuzzware command to the list
def create_output_structure(strategy, target, strategy_config, out_dir, individual_num_runs, debug, runtime, use_python_modeling, exp_name, stats_only):
    commands = []
    # the directory layout is as follows:
    # target path: <out_dir>/<strategy>/<target_name>/<target_name_index>
    # source of the files: <target_name>/
    for i in range(0,individual_num_runs):
        # target is an absolute path, so get the last fragment
        frag = os.path.basename(target)
        target_path = f"{out_dir}/{exp_name}/{strategy}/{frag}/{frag}-{i}/"
        # check and setup the path
        if os.path.exists(target_path):
            print(f"{target_path} already exists, skipping creation/files setup")
        else:
            if debug == 1:
                pass
            else:
                os.makedirs(target_path)
        command = add_fuzzware_commands(strategy, target_path, target, strategy_config, runtime, use_python_modeling, stats_only)
        commands.append(command)
    return commands


# collect all configs for the specified strategy and build fuzzware commands 
# that run this scenario
# return them in a list
def prepare_runs(strategy, strategy_config, out_dir, individual_num_runs, debug, in_path, targets, runtime, use_python_modeling, exp_name, stats_only):
    # get all directories that contain "config.yml" and are not in the out_dir 
    target_dirs = []
    jobs = []
    print(in_path)
    for subdir, dirs, files in os.walk(in_path):
        if "output" in subdir:
            continue
        # filter all paths that do not contain the targets from the config
        do_analysis=False
        for target in targets:
            if target in subdir:
                print(target, subdir)
                do_analysis=True
        if not do_analysis:
            continue
        for file in files:
            if file == strategy_config and not out_dir in subdir:
                target_dirs.append(subdir)
    for target in target_dirs: 
        commands = create_output_structure(strategy, target, strategy_config, out_dir, individual_num_runs, debug, runtime, use_python_modeling, exp_name, stats_only)
        jobs += commands
    return jobs


def parse_config(basedir, config_name=".config.yml"):
    res = None
    with open(f"{basedir}/{config_name}", 'r') as f:
        res = yaml.safe_load(f)
    assert(res)
    return res
