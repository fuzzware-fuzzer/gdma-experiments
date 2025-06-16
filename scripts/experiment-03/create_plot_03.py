import matplotlib.pyplot as plt
import numpy as np
import csv
import argparse
from pathlib import Path
import os
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

NUM_TARGETS=10
MARKERSIZE=3
SAMPLING = 60

GDMA_LABEL = "Fuzzware + GDMA"
FUZZWARE_LABEL = "Fuzzware"

GDMA_MARKER='o'
FUZZWARE_MARKER='x'

def read_file(path):
    res = []
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in spamreader:
            if row[0].startswith("#"):
                continue
            res.append((int(row[0]),int(row[1])))
    return res


# the easiest way to plot is if we have a data point for every second
# the file does not have it, so we pad it
# if we have n blocks at time t0, and the next entry is at t1, we 
# assign n for every point in time between t0 and t1
# however to reduce the number of sample points and the filesize
# we sample only every SAMPLING seconds
def pad(data, runtime):
    print(f"Runtime: {runtime}")
    padded_data = []
    current_index = 0
    last_time = 0 
    last_numblocks = 0
    times = [x[0] for x in data]
    numblocks = [x[1] for x in data]
    cur_index = 0
    for i in range(0, (runtime + 1)):
        if cur_index < len(times):
            if i == times[cur_index]:
                padded_data.append((i, numblocks[cur_index]))
                last_numblock = numblocks[cur_index]
                cur_index += 1
                continue
        padded_data.append((i, last_numblock))

    sampled_data = []

    for time, numblocks in padded_data:
        if time % SAMPLING == 0:
            sampled_data.append((time, numblocks))

    return sampled_data
    #return padded_data


# they are still all called T1-T6, replace to m1-3 r1-3
def update_target_name(old_name):
    old_name = old_name.replace("T1","M1")
    old_name = old_name.replace("T2","M2")
    old_name = old_name.replace("T3","M3")
    old_name = old_name.replace("T4","R1")
    old_name = old_name.replace("T5","R2")
    old_name = old_name.replace("T6","R3")
    return old_name


def build_turned_plot(nodma_data, dma_data, runtime):
    fig, ax = plt.subplots(NUM_TARGETS//2, 2, figsize=(6.5,8))
    color_nodma = "#5F9ED1" # blue
    color_dma = "#ABABAB" # very light gray
    color_dice = "#FF800E" # orange

    index = 0
    targets_sorted = list(nodma_data.keys())
    targets_sorted.sort()
    # keys are all the same, so pick any
    for target in targets_sorted:
        print(f"target: {target}")
        nodma_avg, nodma_min, nodma_max = nodma_data[target]
        dma_avg, dma_min, dma_max = dma_data[target]

        # convert lists to numpy array
        np_nodma_avg = np.array(nodma_avg)
        np_nodma_min = np.array(nodma_min)
        np_nodma_max = np.array(nodma_max)

        # convert lists to numpy array
        np_dma_avg = np.array(dma_avg)
        np_dma_min = np.array(dma_min)
        np_dma_max = np.array(dma_max)
        
        # time scale as np object
        runtime_s = runtime * 3600
        time_scale_nodma_np = np.arange(0,(runtime_s + 1), SAMPLING)
        time_scale_dma_np = np.arange(0,(runtime_s + 1), SAMPLING)


        ax = fig.axes[index] 

        # set the name
        ax.set_title(update_target_name(target))
        
        # draw the error for nodma
        ax.fill_between(time_scale_nodma_np, np_nodma_min, np_nodma_max, color=color_nodma, alpha=0.2)
        # plot line 1
        without_dma, = ax.plot(time_scale_nodma_np, np_nodma_avg, color=color_nodma, label=FUZZWARE_LABEL, marker=FUZZWARE_MARKER, markevery=(120, 240),markersize=MARKERSIZE)

        # set scale to hours on axis
        hours = []
        # we want 4 entries
        num_hours = runtime/4 

        # time scale for labels as np object
        time_labels = np.arange(0,(runtime_s+1), 3600*num_hours)

        for i in range(0,runtime_s+1):
            if i % (3600*num_hours) == 0:
                hours.append(i//3600)
        # it can technically happen that we are missing the 24h entry
        # add it if it is missing
        if len(hours) < runtime/num_hours+1:
            hours.append(runtime)
        ax.set_xticks(time_labels,hours)

        if index >= 8:
            ax.set_xlabel("time (h)")
            #ax.xaxis.set_label_coords(0.5, -0.2)
        
        # set the y label
        # only for the leftmost plots
        if (index%2) == 0:
            ax.set_ylabel("# blocks covered")
            ax.yaxis.set_label_coords(-0.2, 0.5)
        
        # draw the error for dma
        ax.fill_between(time_scale_dma_np, np_dma_min, np_dma_max, color=color_dma,alpha=0.2)
        # plot line 2
        with_dma,  = ax.plot(time_scale_dma_np, np_dma_avg, color=color_dma,label=GDMA_LABEL, marker = GDMA_MARKER, markevery=(0, 240), markersize=MARKERSIZE)



        index += 1



    dma_patch = mpatches.Patch(color=color_dma, label=GDMA_LABEL)
    nodma_patch = mpatches.Patch(color=color_nodma, label=FUZZWARE_LABEL)
    dma_patch = mlines.Line2D([], [], color=color_dma, marker=GDMA_MARKER, linestyle='None', markersize=10, label=GDMA_LABEL)
    nodma_patch = mlines.Line2D([], [], color=color_nodma, marker=FUZZWARE_MARKER, linestyle='None', markersize=10, label=FUZZWARE_LABEL)
    # set manual legend handles
    labels=[GDMA_LABEL, FUZZWARE_LABEL]
    fig.legend(handles=[dma_patch, nodma_patch],ncol=2, bbox_to_anchor=(0.85, 0.02))
    fig.tight_layout()
    plt.savefig('03-cov.png', bbox_inches="tight")
    plt.savefig('03-cov.pdf', bbox_inches="tight")
    plt.show()

            
def build_plot(nodma_data, dma_data, runtime):
    runtime_s = runtime*3600
    fig, ax = plt.subplots(2,NUM_TARGETS//2, figsize=(12.5, 4))
    color_nodma = "#5F9ED1" # blue
    color_dma = "#ABABAB" # very light gray
    color_dice = "#FF800E" # orange

    # nice, our sorting was non-deterministic. So we need to hardcode it now to keep it the same as in the paper
    sorted_keys = ["T2-zephyr-6lowpan", "T3-mcuxpresso-cat", "T4-modus-toolbox-json", "T5-sam3x-x509", "T6-renesas-picohttp", "T2-contiki-6lowpan", "T3-mbed-bluetooth", "T4-efm32-mqtt", "T5-mcuxpressoide-ss7", "T6-renesas-hci"]

    index = 0
    # keys are all the same, so pick any
    for target in sorted_keys:
        nodma_avg, nodma_min, nodma_max = nodma_data[target]
        dma_avg, dma_min, dma_max = dma_data[target]

        # convert lists to numpy array
        np_nodma_avg = np.array(nodma_avg)
        np_nodma_min = np.array(nodma_min)
        np_nodma_max = np.array(nodma_max)

        # convert lists to numpy array
        np_dma_avg = np.array(dma_avg)
        np_dma_min = np.array(dma_min)
        np_dma_max = np.array(dma_max)
        
        # time scale as np object
        time_scale_nodma_np = np.arange(0,(runtime_s+ 1), SAMPLING)
        time_scale_dma_np = np.arange(0,(runtime_s+ 1), SAMPLING)


        ax = fig.axes[index] 

        # set the name
        ax.set_title(update_target_name(target))
        
        # draw the error for nodma
        ax.fill_between(time_scale_nodma_np, np_nodma_min, np_nodma_max, color=color_nodma, alpha=0.2)
        # plot line 1
        without_dma, = ax.plot(time_scale_nodma_np, np_nodma_avg, color=color_nodma, label=FUZZWARE_LABEL, marker=FUZZWARE_MARKER, markevery=(120, 240),markersize=MARKERSIZE)

        # set the x label
        # only for the second to last plot
        if index >= 5:
            ax.set_xlabel("time (h)")


        # set scale to hours on axis
        hours = []
        num_hours = runtime/4 

        # time scale for labels as np object
        time_labels = np.arange(0,(runtime_s+1), 3600*num_hours)

        for i in range(0,runtime_s+1):
            if i % (3600*num_hours) == 0:
                hours.append(i//3600)
        # it can technically happen that we are missing the 24h entry
        # add it if it is missing
        if len(hours) < runtime/num_hours+1:
            hours.append(runtime)
        ax.set_xticks(time_labels,hours)

        # set the y label
        # only for the leftmost plots
        if index == 0 or index == 5:
            ax.set_ylabel("# blocks covered")
        
        # draw the error for dma
        ax.fill_between(time_scale_dma_np, np_dma_min, np_dma_max, color=color_dma,alpha=0.2)
        # plot line 2
        with_dma,  = ax.plot(time_scale_dma_np, np_dma_avg, color=color_dma,label=GDMA_LABEL, marker = GDMA_MARKER, markevery=(0, 240), markersize=MARKERSIZE)



        index += 1

    dma_patch = mpatches.Patch(color=color_dma, label=GDMA_LABEL)
    nodma_patch = mpatches.Patch(color=color_nodma, label=FUZZWARE_LABEL)
    dma_patch = mlines.Line2D([], [], color=color_dma, marker=GDMA_MARKER, linestyle='None', markersize=10, label=GDMA_LABEL)
    nodma_patch = mlines.Line2D([], [], color=color_nodma, marker=FUZZWARE_MARKER, linestyle='None', markersize=10, label=FUZZWARE_LABEL)
    # set manual legend handles
    labels=[GDMA_LABEL, FUZZWARE_LABEL]
    fig.legend(handles=[dma_patch, nodma_patch],ncol=2, bbox_to_anchor=(0.65, 0.03))
    fig.tight_layout()
    plt.savefig('03-cov.png', bbox_inches="tight")
    plt.savefig('03-cov.pdf', bbox_inches="tight")
    plt.show()



def parse_runtime(path):
    try:
        with open(path, "r") as rt:
            # we expect 3 lines
            data = rt.readlines()
            assert len(data) == 3, "unexpected fuzzware runtime format"
            # line two: start_epoch_seconds: <number>
            start_time = int(data[1].strip().split(": ")[1])
            # line three: end_epoch_seconds: <number>
            end_time = int(data[2].strip().split(": ")[1])
            return end_time - start_time
    except Exception as e:
        print(f"Runtime file at {path} not existing or in wrong format")


def build_run_csv(padded_data, suffix):
    with open(f"03_stats_{suffix}.csv","w") as f:
        csv_writer = csv.writer(f)
        # header: target,run,#blocks
        csv_writer.writerow(["Target","Run","#Blocks"])
        for target in padded_data.keys():
            runs = padded_data[target]
            for i in range(0,len(runs)):
                csv_writer.writerow([target,str(i),runs[i][-1][1]])

# we load the coverage info of all target dirs
# and we pad the length to the biggest number 
# we encounter in column 0
def collect_and_pad_coverage_info(target_name, target_dirs, runtime):
    cov = []
    target_dirs.sort()
    # collect all coverage info
    for target_dir in target_dirs:
        cov_path = os.path.join(target_dir, "stats", "covered_bbs_by_second_into_experiment.csv")

        try:
            # this returns a list of tuples with (time, #cov blocks)
            # read_file already removes empty spaces between points
            # in time, but not at the end
            cov.append(pad(read_file(cov_path), runtime))
        except Exception as e:
            print(e)
            print(f"Cov path {cov_path} does not exist")
    return cov


# take a target name and its dirs to collect
# longest runtime and averaged coverage info
# we need the longest runtime to pad our data later for matplotlib
def load_project_runtime_fuzzware(target_name, target_dirs):
    max_runtime = 0
    for d in target_dirs:
        # compute runtime
        runtime_path = os.path.join(d, "logs", "runtime.txt")
        runtime = parse_runtime(runtime_path)
        if runtime:
            max_runtime = max(max_runtime, runtime)
        else:
            print(f"Failed to parse runtime of run {d}")
    return max_runtime



# take a path to a dir with fuzzware data (e.g. a no-dma path)
def load_data_fuzzware(path, num_runs, runtime):
    # a list of all fuzzware-project dirs
    projects = []
    # a dict that maps target names to folders containing runs for that target
    target_map = {}
    # loading data from fuzzware starts with finding all fuzzware-project dirs
    for root, d, files in os.walk(path):
        root = Path(root)
        if root.name == "fuzzware-project":
            projects.append(root)
    for project in projects:
        # the grandparent's name is the target name
        target_name = project.parent.parent.name
        try:
            tmp = target_map[target_name]
        except:
            target_map[target_name] = []
        target_map[target_name].append(project)
    target_cov = {} 
    for target in target_map.keys():
        # return the longest runtime of all runs in seconds
        # required for padding the data to that length
        longest_runtime = load_project_runtime_fuzzware(target, target_map[target])
        # return a list of lists
        # each list contains tuples (time,#blocks covered) per target
        # if we only want stats for less than longest runtime, reduce longest_runtime
        rt = min(runtime*3600, longest_runtime)
        cov_info = collect_and_pad_coverage_info(target, target_map[target], rt)
        assert len(cov_info) == num_runs, "Failed to parse some of the runs"

        # at this point, we know the maximum runtime and have the cov data parsed
        # now pad the cov data to the runtime
        
        # sometimes, we run a little bit over as fuzzware does not terminate
        # immediately. ignore that in coverage, there is no new coverage
        # anyways
        

        # the cov_info runs are padded in-place, so we just use it
        # at this point as the final result value
        
        target_cov[target] = cov_info

    for k in target_cov.keys():
        l = len(target_cov[k][0])
        for run in target_cov[k]:
            assert len(run) == l, f"found different sizes for different runs on the same target, expected {l}, got {len(run)}"
    return target_cov


# we get a dict of padded data as prepared by load_data_fuzzware
# which represents all runs
# compute median and percentiles
def compute_statistics(padded_data):
    stat_data = {}
    for target in padded_data.keys():
        target_avg = []
        target_min = []
        target_max = []
        runs = padded_data[target]
        np_runs = np.array([[x[1] for x in l] for l in runs])
        median = np.median(np_runs, axis =0)
        target_min = np.percentile(np_runs, 25, axis=0)
        target_max = np.percentile(np_runs, 75, axis=0)
        stat_data[target] = (median, target_min, target_max)
    return stat_data

def main(args):
    # first step: load the required data

    # nodma data
    padded_nodma = load_data_fuzzware(args.no_dma_cov, args.num_runs, args.runtime)
    if args.stats:
        build_run_csv(padded_nodma,"nodma")
    stat_nodma = compute_statistics(padded_nodma)
    # dma data
    padded_dma = load_data_fuzzware(args.dma_cov, args.num_runs, args.runtime)
    if args.stats:
        build_run_csv(padded_dma,"dma")
    stat_dma = compute_statistics(padded_dma)
    if args.turn:
        build_turned_plot(stat_nodma, stat_dma, args.runtime)
    else:
        build_plot(stat_nodma, stat_dma, args.runtime)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='fuzzing-plots')
    parser.add_argument('--no-dma-cov', type=Path, required=True, default=None, help="Path to no-dma dir")
    parser.add_argument('--dma-cov', type=Path, required=True, default=None, help="Path to dir with a dma technique enabled (manual-generic or automatic-generic)")
    parser.add_argument('--num-runs', type=int, required=False, default=5, help="Path to dir with a dma technique enabled (manual-generic or automatic-generic)")
    parser.add_argument('--stats', default=False, action="store_true", help="Generate stats per run csv")
    parser.add_argument('--turn', default=False, action="store_true", help="turn layout from 5x2 to 2x5")
    parser.add_argument('--runtime', type=int, default=24, help="runtime in hours")
    args = parser.parse_args()
    main(args)
