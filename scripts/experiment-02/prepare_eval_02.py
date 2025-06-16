import subprocess
from pathlib import Path
import argparse
import os
import shutil
import hashlib



# walk in_path, find all elfs, and record their relative path from in_path - the final `output/`
# also record the target paths
# returns a list of (source,destination) tuples
def collect_elfs(in_path, out_path):
    result = []
    for d, dirs, files in os.walk(in_path):
        for file in files:
            if ".elf" in file:
                file_path = os.path.join(d,file)
                build_bin(file_path)
                file_path = file_path[:-3] + "bin"
                # remove the lowest-level folder ("output")
                d = os.path.dirname(d)
                relpath = os.path.relpath(d,start=in_path)
                target_dir = os.path.join(out_path, relpath, file)
                target_dir = target_dir[:-3] + "bin"
                result.append((file_path, target_dir))
    return result


# takes a path of elfs and builds bins
def build_bin(elf):
    bin_name = elf[:-3] + "bin"
    cmd = ["arm-none-eabi-objcopy", "-O" ,"binary", elf, bin_name]
    subprocess.run(cmd)


# execute fuzzware genconfig
# path is the elf path
def generate_config(p):
    # first, build the bin file with objectcopy
    bin_file = p[:-3]+"bin"
    cmd = ["arm-none-eabi-objcopy","-O","binary", p, bin_file]
    subprocess.run(cmd)
    parent_dir = Path(p).parent
    # try removing the config_autogen.yml if it exists
    autogen = parent_dir / "config_autogen.yml"
    if os.path.isfile(autogen):
        os.unlink(autogen)
    cmd = ["fuzzware", "genconfig" ,"-o", str(autogen), p]
    subprocess.run(cmd)


# we need to remove the .bin file if it exists
# path is the destination elf path
def remove_files_if_exists(path):
    parent = Path(path).parent
    filename = Path(path).name # this ends in .elf, we remove elf and check for bin
    filename = filename[:-3] + "bin"
    p = parent / filename
    print(f"Removing {p}")
    if os.path.isfile(p):
        os.unlink(p)
    elf = filename[:-3] + "elf"
    p = parent / elf
    print(f"Removing {p}")
    if os.path.isfile(p):
        os.unlink(p)


# takes a list of (source,destination)
# copies source to destination if destination does not exist
# if it exists and the md5 matches, skip it
# if it exists and the md5 does not match, overwrite it
def copy_to_new_location(target_list, update):
    for src, dst in target_list:
        # case 1: target does not exist
        if not os.path.exists(dst):
            print(f"{dst} requires update (does not exist)")
            if update:
                print(f"Updating {dst}")
                remove_files_if_exists(dst)
                elf_src = src[:-3] + "elf"
                elf_dst = dst[:-3] + "elf"
                shutil.copy2(elf_src,elf_dst)
                # shutil.copy2(src,dst)
                print("Generating new config_autogen.yml")
                generate_config(elf_dst)
        # case 2: it exists
        else:
            src_md5 = hashlib.md5(open(src,'rb').read()).hexdigest()
            dst_md5 = hashlib.md5(open(dst,'rb').read()).hexdigest()
            # 2.1: md5 matches, do nothing
            if src_md5 == dst_md5:
                print(f"Hash of {dst} matches built binary, skipping")
                continue
            # 2.2: md5 does not match, remove old elf/bin, copy new and generate config
            # removing an old one if it existed
            else:
                print(f"Hash of {dst} differs")
                if update:
                    print(f"Updating {dst}")
                    remove_files_if_exists(dst)
                    elf_src = src[:-3] + "elf"
                    elf_dst = dst[:-3] + "elf"
                    shutil.copy2(elf_src,elf_dst)
                    print("Generating new config_autogen.yml")
                    generate_config(elf_dst)


def main(args):
    elfs = collect_elfs(args.in_path, args.out_path)
    copy_to_new_location(elfs, args.update)


if __name__ == "__main__":
    ROOT = Path(os.path.realpath(__file__)).parent.parent.parent
    parser = argparse.ArgumentParser(prog='Elf-updater', description='Checks if the current elf files in the eval dir match the ones from the source dir')
    parser.add_argument('-u', '--update',  action='store_true', help='overwrite elfs in-place instead of reporting')
    parser.add_argument('-i', '--in-path', required=False, type=Path, default=f"{ROOT}/src/02-extended-test-suite/", help='Path that contains sources to build')
    parser.add_argument('-o', '--out-path', required=False, type=Path, default=f"{ROOT}/02-extended-test-suite/", help='Path to move new elfs to')
    args = parser.parse_args()
    main(args)
