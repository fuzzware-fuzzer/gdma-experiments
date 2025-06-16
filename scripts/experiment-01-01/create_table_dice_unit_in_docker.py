import subprocess
import os
from pathlib import Path
import argparse

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
    if args.latex:
        run_fuzzware_docker(["/bin/bash", "scripts/experiment-01-01/create_table_dice_unit.sh", "01-dice-comparison/01-unit-tests/output/dice-unit/automatic-generic-dma/", "--latex"], 1, 0, True)
    else:
        run_fuzzware_docker(["/bin/bash", "scripts/experiment-01-01/create_table_dice_unit.sh", "01-dice-comparison/01-unit-tests/output/dice-unit/automatic-generic-dma/"], 1, 0, True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Table-creator',
                    description='Docker wrapper to create unit test table')
    parser.add_argument('--latex', action='store_true')
    # command, num cores, starting core id, run synchronous
    args = parser.parse_args()
    main(args)
