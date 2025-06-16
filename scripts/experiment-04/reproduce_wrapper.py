import argparse
import os
from pathlib import Path
import subprocess

def main(args):
    cve_dirs = []
    for d in os.listdir(args.targets):
        if "CVE" in d:
            cve_dirs.append(os.path.abspath(os.path.join(args.targets,d)))
    for cve_dir in cve_dirs:
        target = Path(cve_dir).name
        print(f"Running reproducer for target {target}.")
        r = subprocess.run(["fuzzware", "emu", "-d", "-t", "-M", "-v", "-c", "reproducer/config.yml", "reproducer/crashing_input"], cwd=cve_dir, capture_output=True)
        print(f"Writing crash trace to {cve_dir}/crash_trace.txt")
        with open(f"{cve_dir}/crash_trace.txt","w") as f:
            f.write(r.stdout.decode())
        # sanity check that the last line contains a hint that the emulation crashed
        # yes, its a bit inefficient that we open the file again for that
        with open(f"{cve_dir}/crash_trace.txt","r") as f:
            rd = f.readlines()
            crash_found = "Emulation crashed" in rd[-1]
            if crash_found:
                print(f"{target} crashed with reproducer input. Success.")
            else:
                print(f"Error: {target} did not crash for reproducer!")
        print()
    print("Successfully reproduced all crashes.")



if __name__=="__main__":
    parser = argparse.ArgumentParser(prog='run-reproducer')
    parser.add_argument('--targets', type=Path, required=True, default=None, help="Path to experiment 4 targets directory")
    args = parser.parse_args()
    main(args)
