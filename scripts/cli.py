#! /usr/bin/env python3 
import argparse
import sys
import subprocess
from pathlib import Path
import os
import importlib


# names for subfunctions

# run all experiments
MODE_RUN_EXPERIMENTS = "run-experiments"
# create unit test table
MODE_UNIT_TABLE = "eval-1-1"
# generate dice fuzzing plot
MODE_DICE_FUZZING = "eval-1-2"
# evaluate experiment 2 results
MODE_EVAL_2 = "eval-2"
# evaluate experiment 2 false positives 
MODE_EVAL_2_FP = "eval-2-fp"
# build experiment 2 data set 
MODE_BUILD_2 = "build-2"
# update experiment 2 data set 
MODE_UPDATE_2 = "update-2"
# generate real world plot
MODE_REALWORLD_FUZZING = "eval-3"
# build experiment 3 data set 
MODE_BUILD_3 = "build-3"
# update experiment 3 data set 
MODE_UPDATE_3 = "update-3"
# run reproducers and check that they do indeed crash
MODE_BUGS = "eval-4"
# run reproducers and check that they do indeed crash
MODE_BUGS_HOOKS = "eval-4-hooks"
# evaluate false positive (experiment 5) experiment
MODE_FALSE_POSITIVE = "eval-5"
# rerun dice and p2im on 1-2 targets
MODE_RERUN_DICE = "run-dice"

# root directory of the artifact eval
DIR = Path(os.path.realpath(__file__)).parent.parent


def check_docker_image():
    r = subprocess.run(["docker","images", "-q", "fuzzware:latest"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    return r.stdout != b""
    

def rebuild_2(args):
    if args.use_docker and args.export_images:
        print("Cannot import and export images at the same time.")
        exit()
    build_script_path = f"{DIR}/src/02-extended-test-suite/build_all_samples.sh"
    env = {}
    if args.use_docker:
        env["IMPORT_IMAGES"] = "1"
    if args.export_images:
        env["EXPORT_IMAGES"] = "1"
    subprocess.run(["sh", build_script_path], env=env)


def update_2(args):
    if args.update and args.print_diffs:
        print("Can only specify one of --update and --print-diffs")
        exit()
    if args.update:
        update = importlib.import_module("experiment-02.prepare_eval_02_docker")
        fake_args = argparse.Namespace(name="", update=True)
        update.main(fake_args)
    if args.print_diffs:
        print("running print diffs")
        update = importlib.import_module("experiment-02.prepare_eval_02_docker")
        fake_args = argparse.Namespace(name="", update=False)
        update.main(fake_args)


def update_3(args):
    if args.update and args.print_diffs:
        print("Can only specify one of --update and --print-diffs")
        exit()
    if args.update:
        update = importlib.import_module("experiment-03.prepare_eval_03_docker")
        fake_args = argparse.Namespace(name="", update=True)
        update.main(fake_args)
    if args.print_diffs:
        print("running print diffs")
        update = importlib.import_module("experiment-03.prepare_eval_03_docker")
        fake_args = argparse.Namespace(name="", update=False)
        update.main(fake_args)




def rebuild_3(args):
    if args.use_docker and args.export_images:
        print("Cannot import and export images at the same time.")
        exit()
    build_script_path = f"{DIR}/src/03-coverage-experiments/build_all_samples.sh"
    env = {}
    if args.use_docker:
        env["IMPORT_IMAGES"] = "1"
    if args.export_images:
        env["EXPORT_IMAGES"] = "1"
    subprocess.run(["sh", build_script_path], env=env)


def main():
    parser = argparse.ArgumentParser(description="Gdma reproduction cli", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    def do_help(args):
        parser.parse_args(['-h'])
    subparsers = parser.add_subparsers(title="Components", help='Gdma reproduction utilities:', description="Gdma supports its different functions using a set of utilities.\n\nUse 'cli.py <util_name> -h' for more details.")
    parser.set_defaults(func=do_help)

    # rerun the experiments
    parser_experiment_runner = subparsers.add_parser(MODE_RUN_EXPERIMENTS, help="Rerun experiments.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_experiment_runner.add_argument('-r', '--regen-configs', action='store_true', help="If set, propagate \".experiments-config.yml\" parameters to all experiments. Otherwise use the defaults from the experiment. ")
    parser_experiment_runner.add_argument('-d', '--dry-run', action='store_true', help="If set, print executed commands instead of running them")
    parser_experiment_runner.add_argument('-s', '--stats-only', action='store_true', help="If set, only execute genstats and skip pipeline")
    parser_experiment_runner.add_argument('-vm', '--disable-scaling-governor-check', action='store_true', help="If set, set AFL_SKIP_CPUFREQ=1 to disable checks for the correct scaling governor check")
    
    repro = importlib.import_module("reproduce_experiments")
    parser_experiment_runner.set_defaults(func=repro.main)
   
    # eval experiment 1-1
    # create table for dice unit tests
    parser_unit_table= subparsers.add_parser(MODE_UNIT_TABLE, help="Build the unit test table (Table 7) in docker.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_unit_table.add_argument('--latex', action='store_true')
    unit_table = importlib.import_module("experiment-01-01.create_table_dice_unit_in_docker")
    parser_unit_table.set_defaults(func=unit_table.main)
    
    # eval experiment 1-2 
    # create dice fuzzing plots 
    parser_dice_fuzzing = subparsers.add_parser(MODE_DICE_FUZZING, help="Build the plots for the dice fuzzing targets (Figure 7).", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_dice_fuzzing.add_argument('--dice-cov', type=Path, required=False, default=f"{DIR}/01-dice-comparison/02-real-firmware/02-results/DICEFuzzBase/", help="Path to dice coverage")
    parser_dice_fuzzing.add_argument('--p2im-cov', type=Path, required=False, default=f"{DIR}/01-dice-comparison/02-real-firmware/02-results/P2IMFuzzBase/", help="Path to p2im coverage")
    parser_dice_fuzzing.add_argument('--no-dma-cov', type=Path, required=False, default=f"{DIR}/01-dice-comparison/02-real-firmware/output/dice-fuzzing/no-dma/", help="Path to no-dma dir")
    parser_dice_fuzzing.add_argument('--dma-cov', type=Path, required=False, default=f"{DIR}/01-dice-comparison/02-real-firmware/output/dice-fuzzing/automatic-generic-dma/", help="Path to dir with dma enabled")
    parser_dice_fuzzing.add_argument('--num-runs', type=int, required=False, default=5, help="Number of iterations per target")
    parser_dice_fuzzing.add_argument('--runtime', type=int, required=False, default=24, help="Execution time per run")
    parser_dice_fuzzing.add_argument('--stats', default=False, action="store_true", help="Generate stats per run csv")
    
    dice_fuzzing_plot = importlib.import_module("experiment-01-02.create_plot_dice_fuzzing")
    parser_dice_fuzzing.set_defaults(func=dice_fuzzing_plot.main)
    
    # eval experiment 2
    # check for discovered password characters in eval 2
    parser_eval_2 = subparsers.add_parser(MODE_EVAL_2, help="Checks that each target in experiment 2 found password characters.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_eval_2.add_argument('--results', type=Path, required=False, default=f"{DIR}/02-extended-test-suite/results_experiment_02.yml", help="The path to the results_experiment_02.yml")
    
    eval_2 = importlib.import_module("experiment-02.eval_experiment_2")
    parser_eval_2.set_defaults(func=eval_2.main)
    
    # eval 2 fp 
    parser_fp_2 = subparsers.add_parser(MODE_EVAL_2_FP, help="Checks that each target in experiment 2 found the correct DMA config.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_fp_2.add_argument('--data', type=Path, default="02-extended-test-suite/output/02-dataset/automatic-generic-dma/", help="Path to eval results relative from project root")
    parser_fp_2.add_argument('--groundtruth-root', type=Path, default="02-extended-test-suite/targets/", help="Path to dir with reference configs")
    parser_fp_2.add_argument('--groundtruth-type', default="refconfig", help="Type of ground truth we have")
    parser_fp_2.add_argument('--ref-name', default="", help="The name of the snippets dir")
    parser_fp_2.add_argument('--name', default="", help="The name of the run")
    
    eval_2_fp = importlib.import_module("false-positive.docker_eval_wrapper")
    parser_fp_2.set_defaults(func=eval_2_fp.main)
    
    # eval experiment 3
    # create plots for real-world targets
    parser_realworld_fuzzing = subparsers.add_parser(MODE_REALWORLD_FUZZING, help="Build the plots for the real world targets (Figure 6).", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser_realworld_fuzzing.add_argument('--no-dma-cov', type=Path, required=False, default=f"{DIR}/03-coverage-experiments/output/03-realworld/no-dma/", help="Path to no-dma dir")
    parser_realworld_fuzzing.add_argument('--dma-cov', type=Path, required=False, default=f"{DIR}/03-coverage-experiments/output/03-realworld/automatic-generic-dma/", help="Path to dir with a dma technique enabled")
    parser_realworld_fuzzing.add_argument('--num-runs', type=int, required=False, default=5, help="Number of runs")
    parser_realworld_fuzzing.add_argument('--stats', default=False, action="store_true", help="Generate stats per run csv")
    parser_realworld_fuzzing.add_argument('--turn', default=False, action="store_true", help="turn layout from 5x2 to 2x5")
    parser_realworld_fuzzing.add_argument('--runtime', type=int, default=24, help="runtime in hours")

    
    realworld_fuzzing = importlib.import_module("experiment-03.create_plot_03")
    parser_realworld_fuzzing.set_defaults(func=realworld_fuzzing.main)

    # eval experiment 4
    # run the crash reproducers and validate that they do crash
    parser_bugs = subparsers.add_parser(MODE_BUGS, help="Rerun crash reproducers to confirm that they crash", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # not putting DIR in the default, as this is a relative path from inside docker
    parser_bugs.add_argument('--targets', type=Path, required=False, default=f"04-finding-new-bugs/targets/", help="Path to targets")

    bugs = importlib.import_module("experiment-04.docker_reproduce_wrapper")
    parser_bugs.set_defaults(func=bugs.main)
    

    # eval experiment 4
    # run the crash reproducers and validate that they do crash
    parser_bugs_hook = subparsers.add_parser(MODE_BUGS_HOOKS, help="Rerun crash reproducers with hooks that print Heureka on bug found. Defaults to reproducer replay.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # not putting DIR in the default, as this is a relative path from inside docker
    parser_bugs_hook.add_argument('--targets', type=Path, required=False, default=f"04-finding-new-bugs/targets/", help="Path to dir")
    parser_bugs_hook.add_argument('-f', '--fuzz', action="store_true", help="If set, start 10 cores 24h fuzzing runs on contiki and mbed 48983 target. Print heureka when bug is found.")
    parser_bugs_hook.add_argument('-d', '--dry-run', action='store_true', help="If set, print executed commands instead of running them")
    parser_bugs_hook.add_argument('-vm', '--disable-scaling-governor-check', action='store_true', help="If set, set AFL_SKIP_CPUFREQ=1 to disable checks for the correct scaling governor check")



    bugs_hook = importlib.import_module("experiment-04.docker_hook_wrapper")
    parser_bugs_hook.set_defaults(func=bugs_hook.main)

    # eval experiment 5
    # check results for false positive experiment 
    parser_false_positives = subparsers.add_parser(MODE_FALSE_POSITIVE, help="Evaluate the false positive experiment.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser_false_positives.add_argument('--results', type=Path, required=False, default=f"{DIR}/05-false-positive/output/", help="The path to the output folder for experiment 5")
    
    false_positives = importlib.import_module("experiment-05.eval_false_positives")
    parser_false_positives.set_defaults(func=false_positives.main)
    

    # build experiment 02 firmwares 
    parser_build_2 = subparsers.add_parser(MODE_BUILD_2, help="Build dataset for experiment 2", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # this translates to an export of IMPORT_IMAGES
    parser_build_2.add_argument('-d', "--use-docker", action="store_true", help="Use prebuilt docker images.")
    parser_build_2.add_argument('-e', "--export-images", action="store_true", help="Export rebuilt docker images.")
    parser_build_2.set_defaults(func=rebuild_2)


    # move 02 experiments to eval paths if the hashes differ
    parser_update_2 = subparsers.add_parser(MODE_UPDATE_2, help="Move new 02 elfs if they differ", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # this translates to an export of IMPORT_IMAGES
    parser_update_2.add_argument('-u', "--update", action="store_true", help="Move built binaries to eval dirs.")
    parser_update_2.add_argument('-pd', "--print-diffs", action="store_true", help="Only show which newly-built binaries differ from their previous versions. Sort of a dry-run for --update")

    parser_update_2.set_defaults(func=update_2)
   
   # build experiment 03 firmwares 
    parser_build_3 = subparsers.add_parser(MODE_BUILD_3, help="Build dataset for experiment 3", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # this translates to an export of IMPORT_IMAGES
    parser_build_3.add_argument('-d', "--use-docker", action="store_true", help="Use prebuilt docker images.")
    parser_build_3.add_argument('-e', "--export-images", action="store_true", help="Export rebuilt docker images.")
    
    parser_build_3.set_defaults(func=rebuild_3)

    # move 03 experiments to eval paths if the hashes differ
    parser_update_3 = subparsers.add_parser(MODE_UPDATE_3, help="Move new 03 elfs if they differ", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # this translates to an export of IMPORT_IMAGES
    parser_update_3.add_argument('-u', "--update", action="store_true", help="Move built binaries to eval dirs.")
    parser_update_3.add_argument('-pd', "--print-diffs", action="store_true", help="Only show which newly-built binaries differ from their previous versions. Sort of a dry-run for --update")

    parser_update_3.set_defaults(func=update_3)
    
    # rerun dice experiment
    parser_rerun_dice = subparsers.add_parser(MODE_RERUN_DICE, help="Rerun dice and p2im for experiment 1-2", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_rerun_dice.add_argument('-d', "--use-docker", action="store_true", help="Use prebuilt docker images.")
    parser_rerun_dice.add_argument('-e', "--export-images", action="store_true", help="Export rebuilt docker images.")

    rerun_dice_func = importlib.import_module("eval-dice.eval_dice")
    parser_rerun_dice.set_defaults(func=rerun_dice_func.main)

    if not check_docker_image():
        print("Could not find fuzzware:latest")
        print("Please make sure that the fuzzware docker image is available!")
        exit()

    args = parser.parse_args()
    print(args)
    args.func(args)

if __name__=="__main__":
    main()
