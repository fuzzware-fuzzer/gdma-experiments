import argparse
import subprocess
import os
import argparse
from pathlib import Path

DIR=Path(os.path.dirname(os.path.realpath(__file__))).parent.parent

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
    if args.update:
        run_fuzzware_docker([ "python3",f"scripts/experiment-02/prepare_eval_02.py", "-u"], 1, 0, True)
    else:
        run_fuzzware_docker([ "python3",f"scripts/experiment-02/prepare_eval_02.py"], 1, 0, True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Docker wrapper for elf updater', description='Checks if the current elf files in the eval dir match the ones from the source dir')
    parser.add_argument('-u', '--update',  action='store_true', help='overwrite elfs in-place instead of reporting')
    args = parser.parse_args()
    main(args)
