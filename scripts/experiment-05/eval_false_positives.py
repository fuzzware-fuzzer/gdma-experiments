from pathlib import Path
import argparse
import os


def main(args):
    found=[]
    print(f"Checking in {args.results} if any target produced a 'dma_config.yml'...")
    for root, dirs, files in os.walk(args.results):
        if "dma_config.yml" in files:
            found.append(os.path.abspath(root/Path("dma_config.yml")))
    if len(found) > 0:
        print("Experiment 5 failed! Found false positives in the following targets:")
        for fp in found:
            print(fp)
    else:
        print("No 'dma_config.yml' found. Experiment 5 passed!")


if __name__=="__main__":
    parser = argparse.ArgumentParser(prog='eval-05', description="Evaluate false positives experiment. This boils down to looking for dma_config.yml files")
    parser.add_argument('--results', type=Path, required=True, default=None, help="The path to the results directory")
    args = parser.parse_args()
    main(args)
