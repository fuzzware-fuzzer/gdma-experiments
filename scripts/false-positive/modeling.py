import subprocess
from multiprocessing import Pool
from typing import Tuple
from tqdm import tqdm

from fuzzware_pipeline.util import find_proj

def add_modelgen_parsing(common_parser, sub_parsers):
    parser = sub_parsers.add_parser("model", help="Generate DMA models", add_help=False, parents=[common_parser])
    parser.set_defaults(func=model_gen_main)

    # parser.add_argument('-o', '--output', type = str, help = "Output file")
    parser.add_argument('--python-modeling', action="store_true", default=False, help="Use python DMA snippet generation instead of the rust-based one.")
    parser.add_argument('--python-summarizing', action="store_true", default=False, help="Use python DMA snippet generation instead of the rust-based one.")
    parser.add_argument('--resume', action="store_true", default=False, help="Skip generating snippets that already exist")
    parser.add_argument('--debug', action="store_true", default=False, help="Display full debug output of DMA snippet generation")
    parser.add_argument('--snip-format', default="bin", choices=("bin", "yaml"), help="Display full debug output of DMA snippet generation")

def model_gen_main(args):
    projdirs = []
    for root_dir in args.root:
        projdirs.extend(find_proj.find_projdirs(root_dir))

    if not projdirs:
        print("Found no project directories. Nothing to do...")
        exit(1)

    print(f"Got {len(projdirs)} project directories")

    if args.name:
        snipdir_postfix = "_" + args.name
    else:
        snipdir_postfix = ""
    num_procs = args.num_cores
    use_python_version = args.python_modeling
    use_python_summary = args.python_summarizing

    need_verbose = args.verbose or args.debug
    snip_format = args.snip_format

    gen_dma_snippets(projdirs, snipdir_postfix, num_procs, use_python_version, use_python_summary, verbose=need_verbose, debug=args.debug, resume=args.resume, snip_format=snip_format)

def pool_func_init(is_verbose=False, is_debug=False, do_resume=False, do_show_in_proj_progress=False, arg_snip_format="bin"):
    global verbose
    global debug
    global resume
    global show_in_proj_progress
    global snip_format
    verbose = is_verbose
    debug = is_debug
    resume = do_resume
    show_in_proj_progress = do_show_in_proj_progress
    snip_format = arg_snip_format

def pool_func_gen_dma_snippets(job):
    global verbose, debug, resume, show_in_proj_progress, snip_format
    projdir, snipdir_postfix, num_procs, use_python_version, use_python_summary = job

    # We are doing subprocesses here as multiprocessing does not like nesting in the same python process
    args = ["fuzzware", "model-dma", "-p", projdir, "--snipdir-postfix", snipdir_postfix, "-n", str(num_procs), "--dma-snippet-format", snip_format]
    if use_python_version:
        args.extend(["--force-python-modeling"])
    if use_python_summary:
        args.extend(["--force-python-summarizing"])
    if debug:
        args.extend(["--debug"])
    if resume:
        args.extend(["--skip-existing"])

    verbose |= show_in_proj_progress
    if verbose:
        # args.extend(["--verbose"])
        subprocess.check_call(args)
    else:
        subprocess.check_call(args, stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def divide_cores(num_cores, num_proj_dirs):
    if num_proj_dirs == 1:
        return 1, num_cores

    num_procs_per_projdir = 1
    if num_cores > num_proj_dirs * 4:
        num_procs_per_projdir = num_cores // num_proj_dirs
    elif num_cores > 4 and num_cores % 4 == 0:
        num_procs_per_projdir = 4
    elif num_cores > 2 and num_cores % 2 == 0:
        num_procs_per_projdir = 2
    num_procs = num_cores // num_procs_per_projdir

    return num_procs, num_procs_per_projdir

def gen_dma_snippets(projdirs, snipdir_postfix, num_cores, use_python_version, use_python_summary, verbose, debug, resume, snip_format):
    jobs = []

    num_procs, num_procs_per_projdir = divide_cores(num_cores, len(projdirs))
    print(f"Using {num_procs} parallel procs with {num_procs_per_projdir} cores per projdir")

    for projdir in projdirs:
        jobs.append((projdir, snipdir_postfix, num_procs_per_projdir, use_python_version, use_python_summary))

    with Pool(num_procs, pool_func_init, [verbose, debug, resume, num_procs == 1, snip_format]) as p:
        it = p.imap(pool_func_gen_dma_snippets, jobs)
        it = tqdm(it, total=len(jobs))
        for res in it:
            pass