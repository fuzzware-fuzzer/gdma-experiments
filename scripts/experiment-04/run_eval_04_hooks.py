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
import subprocess


fuzz_dirs = ["contiki-ng-CVE-2023-48229", "mbed-os-CVE-2024-48981", "mbed-os-CVE-2024-48982", "mbed-os-CVE-2024-48983", "mbed-os-CVE-2024-48985", "mbed-os-CVE-2024-48986"]
all_dirs = ["contiki-ng-CVE-2023-48229", "mbed-os-CVE-2024-48981", "mbed-os-CVE-2024-48982", "mbed-os-CVE-2024-48983", "mbed-os-CVE-2024-48985", "mbed-os-CVE-2024-48986"]


def main(args):
    env = {}
    if args.disable_scaling_governor_check:
        env["AFL_SKIP_CPUFREQ=1"]="1"
    workdir = Path(os.path.dirname(os.path.realpath(__file__)))
    basedir = workdir.parent.parent
    experiment_dir = basedir / Path("04-finding-new-bugs/targets/")
    if args.fuzz:
        for target in fuzz_dirs:
            target = os.path.join(experiment_dir, target)
            script = os.path.join(experiment_dir, "common/fuzz_with_detection.sh")
            cmd = ["bash", script, target]
            if args.dry_run:
                print(cmd)
            else:
                f = open("/tmp/log.txt","w")
                # the fuzzing
                subprocess.run(cmd, cwd=experiment_dir, stdout=f, stderr=subprocess.STDOUT, env=env)
                # grep the tmp file to see if there is heureka
                f.close()
                r = subprocess.run(["grep", "Heureka","/tmp/log.txt"], stdout=subprocess.PIPE, env=env)
                if b"Heureka" in r.stdout:
                    print("Heureka found.")
                    print(f"Successfully reproduced the bug in {target}")
                else:
                    print("Heureka not found, bug needs more time to be discovered.")
    else:
        for target in fuzz_dirs:
            cfg = os.path.join(target,"reproducer/hook_config.yml")
            inp = os.path.join(target,"reproducer/crashing_input")
            script = os.path.join(experiment_dir, "common/reproducer_with_detection.sh")
            cmd = ["bash", script , cfg, inp]
            if args.dry_run:
                print(cmd)
            else:
                r = subprocess.run(cmd, cwd=experiment_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
                if b"Heureka" in r.stdout:
                    print("Heureka found.")
                    print(f"Successfully reproduced the bug in {target}")
                else:
                    print("Heureka not found, bug needs more time to be discovered.")




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
    parser.add_argument('-f', '--fuzz', action='store_true')
    parser.add_argument('-vm', '--disable-scaling-governor-check', action='store_true', help="If set, set AFL_SKIP_CPUFREQ=1 to disable checks for the correct scaling governor check")

    args = parser.parse_args()
    main(args)
