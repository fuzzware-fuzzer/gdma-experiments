import yaml
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


def parse_config(config_name=".config.yml"):
    res = None
    with open(f"{DIR}/05-false-positive/{config_name}", 'r') as f:
        res = yaml.safe_load(f)
    assert(res)
    return res


def main(args):
    config = parse_config()
    command = [ "python3",f"scripts/experiment-05/run_eval_05_fp.py"]
    if args.dry_run:
        command.append("-d")
    if args.stats_only:
        command.append("-s")
    if args.disable_scaling_governor_check:
        command.append("-vm")
    # command, num cores, starting core id, run synchronous
    run_fuzzware_docker(command, 0+config["num_cores"], 0, True)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                prog='Run-05',
                description='Docker wrapper to run experiment 05')
    parser.add_argument('-d', '--dry-run', action='store_true')
    parser.add_argument('-s', '--stats-only', action='store_true')
    parser.add_argument('-vm', '--disable-scaling-governor-check', action='store_true', help="If set, set AFL_SKIP_CPUFREQ=1 to disable checks for the correct scaling governor check")

    # command, num cores, starting core id, run synchronous
    args = parser.parse_args()
    main(args)
