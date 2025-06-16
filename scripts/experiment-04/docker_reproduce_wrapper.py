import yaml
import argparse
from pathlib import Path
import subprocess
import os

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
    # command, num cores, starting core id, run synchronous
    run_fuzzware_docker([ "python3","scripts/experiment-04/reproduce_wrapper.py", "--targets", args.targets], 1, 0, True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='run-reproducer-docker')
    parser.add_argument('--targets', type=Path, required=True, default=None, help="Path to experiment 4 targets directory relative from repo root")
    args = parser.parse_args()
    main(args)
