import matplotlib.pyplot as plt
import statistics
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

NUM_TARGETS=6
MARKERSIZE=3
SAMPLING=60
GDMA_LABEL = "Fuzzware + GDMA"
FUZZWARE_LABEL = "Fuzzware"
DICE_LABEL = "DICE"
P2IM_LABEL = "P2IM"


GDMA_MARKER='o'
FUZZWARE_MARKER='x'
DICE_MARKER='^'
P2IM_MARKER = '+'

def read_file(path):
    res = []
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in spamreader:
            if row[0].startswith("#"):
                continue
            res.append((int(row[0]),int(row[1])))
    return res

def read_file_dice(path):
    res = []
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            if row[0].startswith("#"):
                continue
            res.append((int(row[0]),int(row[1])))
    return res

# the easiest way to plot is if we have a data point for every second
# the file does not have it, so we pad it
# if we have n blocks at time t0, and the next entry is at t1, we 
# assign n for every point in time between t0 and t1
# then sample iut down to decrease time and file size
def pad(data, runtime):
    runtime_s = runtime * 3600
    padded_data = []
    current_index = 0
    last_time = 0 
    last_numblocks = 0
    times = [x[0] for x in data]
    numblocks = [x[1] for x in data]
    cur_index = 0

    for i in range(0, (runtime_s + 1)):
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
            

xdim = 2
ydim = 3
# dimensions
def build_plot(nodma_data, dma_data, dice_data, p2im_data, runtime):
    runtime_s = runtime * 3600
    # https://stackoverflow.com/questions/74830439/list-of-color-names-for-matplotlib-style-tableau-colorblind10
    # plt.style.use('tableau-colorblind10')
    color_nodma = "#5F9ED1" # blue
    color_dma = "#ABABAB" # very light gray
    color_dice = "#FF800E" # orange
    color_p2im = "#A020F0" # purple
    fig, ax = plt.subplots(ydim, xdim, layout='constrained')
    index = 0
    # we did not manually order the plots for the paper, resulting in a random order
    # we need to obtain the same order, so hardcode it
    target_order = ["Soldering-Station", "MIDI-Synthesizer", "Modbus", "Guitar-Pedal", "Stepper-Motor", "GPS-Receiver"]
    for target in target_order:
        nodma_avg, nodma_min, nodma_max = nodma_data[target]
        dma_avg, dma_min, dma_max = dma_data[target]
        dice_avg, dice_min, dice_max = dice_data[target]
        p2im_avg, p2im_min, p2im_max = p2im_data[target]
        

        # convert lists to numpy array
        np_nodma_avg = np.array(nodma_avg)
        np_nodma_min = np.array(nodma_min)
        np_nodma_max = np.array(nodma_max)

        # convert lists to numpy array
        np_dma_avg = np.array(dma_avg)
        np_dma_min = np.array(dma_min)
        np_dma_max = np.array(dma_max)
        
        # convert lists to numpy array
        np_dice_avg = np.array(dice_avg)
        np_dice_min = np.array(dice_min)
        np_dice_max = np.array(dice_max)
        
        # convert lists to numpy array
        np_p2im_avg = np.array(p2im_avg)
        np_p2im_min = np.array(p2im_min)
        np_p2im_max = np.array(p2im_max)

        # time scale as np object
        time_scale_nodma_np = np.arange(0,runtime_s + 1, SAMPLING)
        time_scale_dma_np = np.arange(0,runtime_s + 1, SAMPLING)
        time_scale_dice_np = np.arange(0,runtime_s + 1, SAMPLING)
        time_scale_p2im_np = np.arange(0,runtime_s + 1, SAMPLING)
        
        ax = fig.axes[index] 

        # set the name
        ax.set_title(target)
        
        # plot line 1
        without_dma, = ax.plot(time_scale_nodma_np, np_nodma_avg, color=color_nodma, label=FUZZWARE_LABEL, marker=FUZZWARE_MARKER, markevery=(80, 240), markersize=MARKERSIZE)
        # draw the error for nodma
        ax.fill_between(time_scale_nodma_np, np_nodma_min, np_nodma_max, alpha=0.2, color=color_nodma)
       
        # set the x label
        # only for the second to last plot
        if index >= 4:
            ax.set_xlabel("time (h)")
            ax.xaxis.set_label_coords(0.5, -0.2)
        
        # set the y label
        # only for the leftmost plots
        if (index%2) == 0:
            ax.set_ylabel("# blocks covered")
            ax.yaxis.set_label_coords(-0.2, 0.5)
        
        # plot line 2
        with_dma,= ax.plot(time_scale_dma_np, np_dma_avg, color=color_dma, label=GDMA_LABEL, marker=GDMA_MARKER, markevery=(0,240), markersize=MARKERSIZE)
        # draw the error for dma
        ax.fill_between(time_scale_dma_np, np_dma_min, np_dma_max, alpha=0.2, color=color_dma)

        # set scale to hours on axis
        hours = []
        num_hours = runtime / 4
        
        # time scale for labels as np object
        time_labels = np.arange(0,runtime_s + 1, 3600*num_hours)
        
        for i in range(0,runtime_s + 1):
            if i % (3600*num_hours) == 0:
                hours.append(i//3600)
        # it can technically happen that we are missing the 24h entry
        # add it if it is missing
        if len(hours) < runtime/num_hours+1:
            hours.append(runtime)
        ax.set_xticks(time_labels,hours)

        
        # plot line 2
        dice,  = ax.plot(time_scale_dice_np, np_dice_avg, color=color_dice, label=DICE_LABEL, marker=DICE_MARKER, markevery=(160, 240), markersize=MARKERSIZE)
        # draw the error for dice
        ax.fill_between(time_scale_dice_np, np_dice_min, np_dice_max, alpha=0.2, color=color_dice)
        

        # plot line 2
        p2im,  = ax.plot(time_scale_p2im_np, np_p2im_avg, color=color_p2im, label=P2IM_LABEL, marker=P2IM_MARKER, markevery=(160, 240), markersize=MARKERSIZE)
        # draw the error for p2im
        ax.fill_between(time_scale_p2im_np, np_p2im_min, np_p2im_max, alpha=0.2, color=color_p2im)


        index += 1

        # draw lines/a grid on the graph

    dma_patch = mpatches.Patch(color=color_dma, label=GDMA_LABEL)
    nodma_patch = mpatches.Patch(color=color_nodma, label=FUZZWARE_LABEL)
    dice_patch = mpatches.Patch(color=color_dice, label=DICE_LABEL)
    p2im_patch = mpatches.Patch(color=color_p2im, label=P2IM_LABEL)

    dma_patch = mlines.Line2D([], [], color=color_dma, marker=GDMA_MARKER, linestyle='None', markersize=10, label=GDMA_LABEL)
    nodma_patch = mlines.Line2D([], [], color=color_nodma, marker=FUZZWARE_MARKER, linestyle='None', markersize=10, label=FUZZWARE_LABEL)
    dice_patch = mlines.Line2D([], [], color=color_dice, marker=DICE_MARKER, linestyle='None', markersize=10, label=DICE_LABEL)
    p2im_patch = mlines.Line2D([], [], color=color_p2im, marker=P2IM_MARKER, linestyle='None', markersize=10, label=P2IM_LABEL)
    # set manual legend handles
    labels=[GDMA_LABEL, FUZZWARE_LABEL, DICE_LABEL, P2IM_LABEL ]
    fig.legend(handles=[dma_patch, nodma_patch, dice_patch, p2im_patch],ncol=4, bbox_to_anchor=(0.88, 0.01))
    # print it to stdout
    plt.savefig('dice-fuzzing-cov.png', bbox_inches = 'tight')
    plt.savefig('dice-fuzzing-cov.pdf', bbox_inches = 'tight')
    plt.savefig('dice-fuzzing-cov.svg', bbox_inches = 'tight')
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
            cov.append(pad(read_file(cov_path),runtime))
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
        max_runtime = max(max_runtime, runtime)
    return max_runtime



# no way to extract runtime from dice, but we scheduled it for 24 hours
def load_data_dice(path, num_runs, runtime, scheduled_runtime=86400,):
    # all paths to out.txt files that contain data in a format similar to fuzzware
    file_paths = []
    for root, d, files in os.walk(path):
        if "out.txt" in files:
            file_paths.append(Path(root) / Path("out.txt"))
    target_cov = {}
    for fp in file_paths:
        # get the target name
        target_name = fp.parent.parent.name
        # read the data
        try:
            tmp = target_cov[target_name]
        except:
            target_cov[target_name] = []
        cov_info = pad(read_file_dice(fp), runtime)
        cov_info[0] = (0,0)
        cov_info = cov_info
        starting_length = len(cov_info)
        diff = scheduled_runtime - starting_length
        target_cov[target_name].append(cov_info)
    return target_cov


# no way to extract runtime from dice, but we scheduled it for 24 hours
def load_data_p2im(path, num_runs, runtime, scheduled_runtime=86400):
    # all paths to out.txt files that contain data in a format similar to fuzzware
    file_paths = []
    for root, d, files in os.walk(path):
        if "out.txt" in files:
            file_paths.append(Path(root) / Path("out.txt"))
    target_cov = {}
    for fp in file_paths:
        # get the target name
        target_name = fp.parent.parent.name
        # read the data
        try:
            tmp = target_cov[target_name]
        except:
            target_cov[target_name] = []
        cov_info = pad(read_file_dice(fp), runtime)
        cov_info[0] = (0,0)
        cov_info = cov_info
        starting_length = len(cov_info)
        diff = scheduled_runtime - starting_length
        target_cov[target_name].append(cov_info)
    return target_cov


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
        # return the longest runtime of all runs
        # required for padding the data to that length
        actual_runtime = load_project_runtime_fuzzware(target, target_map[target])
        # return a list of lists
        # each list contains tuples (time,#blocks covered) per target
        cov_info = collect_and_pad_coverage_info(target, target_map[target], runtime)
        assert len(cov_info) == num_runs, "Failed to parse some of the runs"

        # at this point, we know the maximum runtime and have the cov data parsed
        # now pad the cov data to the runtime

        # run_data is data for one run out of <num_runs>
        # the cov_info runs are padded in-place, so we just use it
        # at this point as the final result value
        target_cov[target] = cov_info

    for k in target_cov.keys():
        l = len(target_cov[k][0])
        for run in target_cov[k]:
            assert len(run) == l, f"found different sizes for different runs on the same target, expected {l}, got {len(run)}"
    return target_cov


def build_run_csv(padded_data, suffix):
    with open(f"dice_stats_{suffix}.csv","w") as f:
        csv_writer = csv.writer(f)
        # header: target,run,#blocks
        csv_writer.writerow(["Target","Run","#Blocks"])
        for target in padded_data.keys():
            runs = padded_data[target]
            for i in range(0,len(runs)):
                csv_writer.writerow([target,str(i),runs[i][-1][1]])

# we get a dict of padded data as prepared by load_data_fuzzware
# which represents all runs
# we compute 3 lists:
# the median and the percentiles
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

# this time, we compute the median run as avg, 
# and the two runs closest to the median
# as point of reference, I always take the final
# number of discovered bbs
def compute_statistics_median(padded_data):
    stat_data = {}
    for target in padded_data.keys():
        runs = padded_data[target]
        data = [] 
        # we get the max number of blocks in order 
        for i in range(0,len(runs)):
            # map run indices to # discovered blocks
            # if # discovered blocks is not unique, 
            # we do not care and take the first one
            # get the maximum number of discovered blocks
            _, max_blocks = runs[i][-1]
            data.append(max_blocks)
        # data is ordered in the number of runs thanks to the way it is constructed
        block_median = statistics.median(data)
        
        target_median = None
        try:
            target_median = runs[data.index(block_median)]
        except Exception as e:
            # if we have an even number of runs, the median is
            # apparently the average between both.
            # if that happens, we take the first entry that is larger than
            # the computed median
            for d in data:
                if d > block_median:
                    block_median = d
                    target_median = runs[data.index(d)]
                    break
        # compute the two plots with the smallest distance to the target median

        # take out the one that has the smallest diff to the median
        # only checks diffs for values < median 
        target_1_diff = block_median
        target_1_index = 0 
        for i in range(0,len(runs)):
            # do not count the block median
            if i == data.index(block_median):
                continue
            diff = abs(block_median - data[i])
            if data[i] > block_median:
                target_1_diff = min(diff, target_1_diff)
                # if this updated the diff, update the index
                if target_1_diff == diff:
                    target_1_index = i
        
        # take out the one that has the smallest diff to the median
        # and is not target_1_index
        target_2_diff = block_median
        target_2_index = 0 
        for i in range(0,len(runs)):
            # do not count the block median or target_1_index
            if i == data.index(block_median) or i == target_1_index:
                continue
            diff = abs(block_median - data[i])
            if data[i] > block_median:
                target_2_diff = min(diff, target_2_diff)
                # if this updated the diff, update the index
                if target_1_diff == diff:
                    target_2_index = i
        target_median1d = []
        target_1_1d = []
        target_2_1d = []
        # length is always the same, so should be sane
        for i in range(0,len(runs[0])):
            time, blocks = target_median[i]
            target_median1d.append(blocks)
            time, blocks = runs[target_1_index][i]
            target_1_1d.append(blocks)
            time, blocks = runs[target_2_index][i]
            target_2_1d.append(blocks)
        stat_data[target] = (target_median1d, target_1_1d, target_2_1d)
        print(f"Storing median index {data.index(block_median)} run 1 {target_1_index} run 2 {target_2_index}")
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
    
    # dice data
    # we only have 5 dice runs, so hardcode here
    padded_dice = load_data_dice(args.dice_cov, args.num_runs, args.runtime) 
    stat_dice = compute_statistics(padded_dice)

    # p2im data
    padded_p2im = load_data_dice(args.p2im_cov, args.num_runs, args.runtime) 
    stat_p2im = compute_statistics(padded_p2im)
    # build the final plot
    build_plot(stat_nodma, stat_dma, stat_dice, stat_p2im, args.runtime)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='fuzzing-plots')
    parser.add_argument('--p2im-cov', type=Path, required=True, default=None, help="Path to p2im coverage")
    parser.add_argument('--dice-cov', type=Path, required=True, default=None, help="Path to dice coverage")
    parser.add_argument('--no-dma-cov', type=Path, required=True, default=None, help="Path to no-dma dir")
    parser.add_argument('--dma-cov', type=Path, required=True, default=None, help="Path to dir with a dma technique enabled (manual-generic or automatic-generic)")
    parser.add_argument('--num-runs', type=int, required=False, default=5, help="Number of executions of target")
    parser.add_argument('--runtime', type=int, required=False, default=24, help="Runtime of experiment")
    parser.add_argument('--stats', default=False, action="store_true", help="Generate stats per run csv")
    args = parser.parse_args()
    main(args)
