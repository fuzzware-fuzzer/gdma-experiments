import yaml
import argparse
import subprocess
import os
from pathlib import Path

# the root of the eval
DIR = Path(os.path.realpath(__file__)).parent.parent.parent

# for now, this requires a fuzzware-latest image
def run_fuzzware_docker(cmd_args, max_cores, starting_core_id, run_sync=False):
    docker_cmd_args = [ "docker", "run",
        "--rm", "-it",
        "--user", f"{os.getuid()}:{os.getgid()}",
        "--env", "HOME=/home/user",
        "--env", "PYTHON_EGG_CACHE=/tmp/.cache",
        "--mount", "type=bind,source="+str(DIR)+",target=/home/user/fuzzware/targets",
        "--cpus=" + f"{max_cores:d}",
        "--cpuset-cpus=" + f"{starting_core_id}-{max_cores + starting_core_id-1}",
        "fuzzware:latest"
    ]

    if run_sync:
        return subprocess.run(docker_cmd_args + cmd_args)
    else:
        return subprocess.Popen(docker_cmd_args + cmd_args, preexec_fn=os.setsid)



def main(args):
    command = [ "python3",f"scripts/experiment-04/run_eval_04_hooks.py"]
    if args.dry_run:
        command.append("-d")
    if args.fuzz:
        command.append("-f")
    if args.disable_scaling_governor_check:
        command.append("-vm")
    # we need 10 cores if we do fuzzing
    if args.fuzz:
        # command, num cores, starting core id, run synchronous
        run_fuzzware_docker(command, 10, 0, True)
    else:
        run_fuzzware_docker(command, 1, 0, True)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog='Run-04',
                description='Docker wrapper to run experiment 04')
    parser.add_argument('-d', '--dry-run', action='store_true')

    # command, num cores, starting core id, run synchronous
    args = parser.parse_args()
    main(args)
