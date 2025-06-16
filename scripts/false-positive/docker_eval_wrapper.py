from pathlib import Path
import subprocess
import os
import yaml
import argparse

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
    command = [ "python3",f"scripts/false-positive/cli.py", "diff"]
    command += [str(args.data)]
    command += ["--groundtruth-root",str(f"{args.groundtruth_root}")]
    command += ["--groundtruth-type", args.groundtruth_type]
    command += ["--ref-name", args.ref_name]
    command += ["--name", args.name]
    # command, num cores, starting core id, run synchronous
    run_fuzzware_docker(command, 1, 0, True)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog='Run-fp',
                description='Docker wrapper to run false positive analysis')
    # command, num cores, starting core id, run synchronous
    parser.add_argument('--data', type=Path, required=True, default=None, help="Path to results")
    parser.add_argument('--groundtruth-root', type=Path, required=True, default=None, help="Path to ground truth")
    parser.add_argument('--groundtruth-type', required=True, default=None, help="ground truth type")
    parser.add_argument('--ref-name', required=True, default=None)
    parser.add_argument('--name', required=True, default=None)

    args = parser.parse_args()
    main(args)
