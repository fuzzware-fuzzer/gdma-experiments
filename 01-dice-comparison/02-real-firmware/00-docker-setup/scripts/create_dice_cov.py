import argparse
from pathlib import Path
import os
import stat
import subprocess
from multiprocessing import Pool 
import multiprocessing as mp
import re
import json 


import os
import re
import csv
import ast


bb_file = "bbl_cov"
plot_file = "plot_data"


def _read_cvs_file(path):
    with open(path, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

def _get_creation_ts(id_str, plot_path):
        last = None
        # print(id_str)
        id_ = re.match(r'.*id:([0-9]+)', id_str).group(1).lstrip('0')
        if id_ == '': # id:000000
            id_ = 0
        id_ = int(id_)

        key = ' paths_total'
        # if self.is_crash:
        #     key = ' unique_crashes'
        # elif self.is_hang:
        #     key = ' unique_hangs'

        rows = _read_cvs_file(plot_path)
        for row in rows:
            if int(row[key]) > id_:
                return int(row['# unix_time'])
            last = int(row['# unix_time'])
        assert last is not None
        return last


def create_timings(path):
    bb_file = path + "/coverage/bbl_cov"
    plot_file = path + "/outputs/plot_data"
    dictionary = None
    with open(bb_file,"r") as f:
        dictionary = ast.literal_eval(f.read())

    bbl_creation = {}
    for bbl in dictionary.keys():
        val = dictionary[bbl]
        ts = _get_creation_ts(val, plot_file)
        bbl_creation[bbl] = ts

    min_ts = None
    for bbl in bbl_creation.keys():
        ts = bbl_creation[bbl]
        if not min_ts:
            min_ts = ts
        else:
            min_ts = min(min_ts,ts)

    ts_to_bbs = {}

    for bbl in bbl_creation.keys():
        ts = bbl_creation[bbl] - min_ts
        try:
            tmp = ts_to_bbs[ts]
        except Exception as e:
            ts_to_bbs[ts] = []
        ts_to_bbs[ts].append(bbl)

    # now only need to sum
    ts_to_bbs_sum = []
    curr_sum = 0
    for ts in sorted(ts_to_bbs.keys()):
        curr_sum += len(ts_to_bbs[ts])
        print(curr_sum)
        ts_to_bbs_sum.append((ts,curr_sum))

    with open(f"{path}/out.txt","w") as f:
        for ts, num in ts_to_bbs_sum:
            f.write(f"{ts} {num}\n")
    print(ts_to_bbs_sum)


def setup_projects(root, num_runs):
    projects = {}
    # in the project root, we have a folder per target
    targets = os.listdir(root)
    for target in targets:
        projects[target] = []
        # we thus need <target>/<num>
        # folders are either 1/2/3/4,.. or 1.0/2.0/3.0
        target_root = Path(root) / target
        nums = os.listdir(target_root)
        dice_style = False
        if "1.0" in nums:
            dice_style = True
        for i in range(1,num_runs+1):
            # run_base = target_root / Path(str(i)+".0")
            dir_name = str(i)
            if dice_style:
                dir_name+=".0"
            run_base = target_root / Path(dir_name)
            projects[target].append(run_base)
    return projects


# in p2im/dice, the latest dir is identified as follows (everything is a dirname):
# there are two types of dirs: 
#    flat numbers (0,1,...) 
#    input data dirs (0.input.data.1,0.input.data.2)
# increasing numbers are newer: 
#    1 is newer than 0
#    0.input.data.2 is newer than 0.input.data.1, 
# front is more important than back:
#    1.input.data.1 is newer than 0.input.data.10 
# input.data is more important than flat numbers:
#    0.input.data.1 is newer than 0
def find_latest_dir(path):
    files = os.listdir(path)
    max_num = 0
    for f in files:
        try:
            # we convert the name to int
            # this works for number dirs, everything else raises an Exception
            tmp = int(f)
            max_num = max(tmp,max_num)
        except Exception as e:
            continue
    # we have our biggest number, now we need to check if we have $maxnum.input.data dirs
    special_str = f"{max_num}.input.data"
    special_dirs = []
    for f in files:
        # we collect all dirs that start with "$biggest_num.input.data"
        if f.startswith(special_str):
            special_dirs.append(f)
    special_dirs.sort()
    # now the special_dirs is sorted, and as they are equal except for the last number, 
    # we can take the last list entry if it is not empty
    if len(special_dirs) > 0:
        return special_dirs[-1]
    else:
        return max_num


def rerun_dice_eval(projects, cov_script):
    dice_runs = []
    for target in projects:
        runs = projects[target]
        for run in runs:
            p = find_latest_dir(run)
            # for each run, execute the cov script once
            # Stepper motor hardcode
            dice_runs.append(([cov_script, "-c", "working_cov.cfg","--model-if", f"{p}/peripheral_model.json"], run))
            # dice_runs.append(([p2im_cov_py, "-c", "working_cov.cfg","--model-if", f"{max_num}/peripheral_model.json"], run))
    return dice_runs


# take the cmd list as to pass to subprocess
# and the cwd of the process
def dice_single_run(cmd_list, d):
    print(cmd_list,d)
    subprocess.run(cmd_list,cwd=d)


def main():
    parser = argparse.ArgumentParser(prog='fuzzing-plots')
    parser.add_argument('--data-root', type=Path, required=True, default=None, help="Path to data (dice/p2im) coverage. The directory contains folders which in turn contain the p2im/dice layout")
    parser.add_argument('--cov-script', type=Path, required=True, default=None, help="Path to p2im cov.py")
    parser.add_argument('--num-runs', type=int, required=False, default=10, help="Number of p2im/dice runs per target")
    args = parser.parse_args()
    # prep: setup project
    # a mapping of target name to run root
    projects = setup_projects(args.data_root, args.num_runs)
    runs = rerun_dice_eval(projects, args.cov_script)
    # this used to be multiprocessed, but ran into some concurrency problem
    for run in runs:
        dice_single_run(run[0],run[1])

   # cov gen reran, now we create the coverage over time
    target_paths = []
    targets = os.listdir(args.data_root)
    for target in projects.keys():
        target_paths+=(projects[target])
    print(target_paths)
    for tp in target_paths:
        try:
            create_timings(str(tp))
        except Exception as e:
            print(e)
            continue



if __name__ == "__main__":
    main()
