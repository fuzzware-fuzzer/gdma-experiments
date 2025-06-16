from pathlib import Path
import os
import argparse
import yaml

# the non-contiguous targets 
NON_CONT = ["LPC1837-ram", "MK64F-ram", "SAM3X-ram", "CY8CKIT-062-BLE"]

# we expect some milestones
# we will check if at least two milestones are hit
# at least one milestone shows that dma works,
# at least two shows that the firmware accesses both buffers
# in a non-contiguous scenario
def analyze_dma(data):
    faulty_runs = []
    all_ms_found = True 
    for target in data.keys():
        print(f"Checking if {target} automatic dma has any coverage...")
        if target in NON_CONT:
            print(f"{target} is a scatter gather target. We expect at least two milestones hit.")
        else:
            print(f"{target} is not a scatter gather target. We expect at least one milestone hit.")

        val = data[target]
        run_results = []
        for run in val.keys():
            # we collect the results of each run here. Only one run needs to pass
            # to prove that the mechanism works
            ms_data = val[run]["milestones_covered"]
            ms_sorted = list(ms_data.keys())
            ms_sorted.sort()
            # we inspect the first milestone for all non-sg targets, and the first two for the rest 
            if target in NON_CONT:
                tmp_found = True
                # we inspect the first two milestones for all sg targets 
                for i in range(0,2):
                    k = ms_sorted[i]
                    ms_hit = ms_data[k]
                    if ms_hit == "-1":
                        tmp_found = False
                        faulty_runs.append(target)
                if tmp_found:
                    print(f"Run {run} found all required milestones.")
                all_ms_found = tmp_found
                run_results.append(tmp_found)
            else:
                # we inspect the first milestone for all m targets
                k = ms_sorted[0]
                ms_hit = ms_data[k]
                tmp_found = True
                if ms_hit == "-1":
                    tmp_found = False
                    # we need to track runs that did not reach all milestones, as they will need separate inspection
                    # during false positive analysis later
                    faulty_runs.append(target)
                if tmp_found:
                    print(f"Run {run} found all required milestones.")
                run_results.append(tmp_found)
        if not any(run_results):
            all_ms_found = False
            print(f"No run for target {target} found all required milestones!\nThis should not happen!")
        else:
            print(f"Some runs found all required milestones for target {target}. Test passed.")
            print()
    return all_ms_found, faulty_runs


# we expect zero milestones found
def analyze_nodma(data):
    ms_found = False
    for target in data.keys():
        print(f"Checking if {target} nodma has any milestone coverage...")
        val = data[target]
        for run in val.keys():
            ms_data = val[run]["milestones_covered"]
            ms_sorted = list(ms_data.keys())
            ms_sorted.sort()
            for k in ms_sorted:
                ms_hit = ms_data[k]
                if ms_hit != "-1":
                    print(f"Target {target} run {run} found milestone {k}!\nThis should not happen!")
                    ms_found = True
        if not ms_found:
            print(f"{target} nodma has no milestone coverage. Good.")
    return ms_found


def main(args):
    with open(args.results) as stream:
        try:
            results = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Failed to parse results!\n{exc}")
    nodma_found = analyze_nodma(results["no-dma"])
    if not nodma_found:
        print("Experiment 02 nodma passed.")
    dma_found, faulty_runs = analyze_dma(results["automatic-generic-dma"])
    if dma_found:
        print("Experiment 02 dma passed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='eval-02')
    parser.add_argument('--results', type=Path, required=True, default=None, help="The path to the results_experiment_02.yml")

    args = parser.parse_args()
    main(args)
