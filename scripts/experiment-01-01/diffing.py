from dataclasses import dataclass
from fuzzware_pipeline.util import find_proj, eval_utils
from fuzzware_pipeline.dma.perf_meta import DMAJobPerfResult, DMAJobPerfSummary
from fuzzware_pipeline import naming_conventions as nc
from fuzzware_harness.util import load_config_deep, parse_address_value, parse_symbols
from fuzzware_harness.peripherals.dma.sizerange import SizeRange
import yaml

import os

from typing import Tuple, Dict, List
from pathlib import Path

import logging
logger = logging.getLogger("diffing")
PLACEHOLDER_MMIO_ADDRESS = 0xdeadbeef

REFERENCE_MODEL_FILENAME = "config_generic_dma_manual.yml"
GROUNDTRUTH_YAML_FILENAME = "ground_truth.yml"

GROUNDTRUTH_TYPE_REFERENCE_CONFIG = "refconfig"
GROUNDTRUTH_TYPE_GROUNDTRUTH_YAML = "groundtruth-yaml"

INVALID_DIRNAMES = frozenset(["deprecated", "common"])

def add_modeldiff_parsing(common_parser, sub_parsers):
    parser = sub_parsers.add_parser("diff", help="Diff DMA models against another version", add_help=False, parents=[common_parser]) # , add_help=False
    parser.set_defaults(func=model_diff_main)

    parser.add_argument('--ref-name', type=str, default="", help="Name of the revision to compare / diff results against. Defaults to the original DMA config of the project.")
    parser.add_argument('--groundtruth-root', '-g', type=Path, default=None, help=f"Base directory to find groundtruth files in. Searches for '{REFERENCE_MODEL_FILENAME}' or '{GROUNDTRUTH_YAML_FILENAME}' files, depending on --groundtruth-type.")
    parser.add_argument('--groundtruth-type', '-t', default=GROUNDTRUTH_TYPE_REFERENCE_CONFIG, choices=(GROUNDTRUTH_TYPE_REFERENCE_CONFIG, GROUNDTRUTH_TYPE_GROUNDTRUTH_YAML), help=f"The type of ground-truth data to use ({REFERENCE_MODEL_FILENAME} or {GROUNDTRUTH_YAML_FILENAME})")
    parser.add_argument('--perf', action="store_true", default=False, help="Compare performance metrics")
    parser.add_argument('--file', type=Path, default=None, help="Path to store the diff output to (by project view)")



SEVERITY_LOW    = 10
SEVERITY_MEDIUM = 100
SEVERITY_HIGH   = 1000

@dataclass
class SimpleDMABuf:
    mmio_addr: int
    known_sizes: Dict[int, SizeRange]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        sizes = sorted((self.known_sizes if type(self.known_sizes) == dict else {self.known_sizes: SizeRange()}).items(), key=lambda p: p[0])
        if sizes:
            size_str = ", ".join([f"{buf_addr:#08x}: {sizerange}" for buf_addr, sizerange in sizes])
        else:
            size_str = "<no known sizes>"
        return f"SimpleDMABuf[{self.mmio_addr:#08x}]: " + size_str

class DMAModelDiff:
    severity: int = 0

@dataclass
class DifferentMMIOReg(DMAModelDiff):
    severity = SEVERITY_MEDIUM
    own_mmio_addr: int
    other_mmio_addr: int
    
    def __str__(self) -> str:
        return f"Different MMIO register for same buffer address. {self.own_mmio_addr:#x} vs. {self.other_mmio_addr:#x}"

@dataclass
class DifferentBufferAddresses(DMAModelDiff):
    severity = SEVERITY_MEDIUM
    mmio_address: int
    own_ram_addresses: List[int]
    other_ram_addresses: List[int]

    def __str__(self) -> str:
        return f"Different RAM address for same MMIO register. {','.join(map(hex, self.own_ram_addresses))} vs. {','.join(map(hex, self.other_ram_addresses))} (MMIO address: {self.mmio_address:#x})"

@dataclass
class MissingBufferAddresses(DMAModelDiff):
    severity = SEVERITY_MEDIUM
    mmio_address: int
    missing_ram_addresses: List[int]

    def __str__(self) -> str:
        return f"Missing RAM address for MMIO register. {','.join(map(hex, self.missing_ram_addresses))} (MMIO address: {self.mmio_address:#x})"

@dataclass
class AdditionalBufferAddresses(DMAModelDiff):
    severity = SEVERITY_MEDIUM
    mmio_address: int
    additional_ram_addresses: List[int]

    def __str__(self) -> str:
        return f"Additional RAM address for MMIO register. {','.join(map(hex, self.additional_ram_addresses))} (MMIO address: {self.mmio_address:#x})"

@dataclass
class DifferentSize(DMAModelDiff):
    severity = SEVERITY_LOW
    mmio_address: int
    ram_address: int
    size: SizeRange
    other_size: SizeRange

    def __str__(self) -> str:
        diff_str = ""
        if self.size.minsize != self.other_size.minsize:
            diff_str += f" Minsize {self.size.minsize} vs. {self.other_size.minsize}"
        if self.size.maxsize != self.other_size.maxsize:
            if diff_str:
                diff_str += " |"
            diff_str += f" Maxsize {self.size.maxsize} vs. {self.other_size.maxsize}"
        return f"Different size for {self.ram_address:#x}: {diff_str} (MMIO reg: {self.mmio_address:#x})"

@dataclass
class MissingDescriptor(DMAModelDiff):
    severity = SEVERITY_HIGH
    mmio_address: int
    ram_addresses: List[int]

    def __str__(self) -> str:
        return f"Missing MMIO Register: {self.mmio_address:#x} -> {','.join([hex(addr) for addr in self.ram_addresses])}"

@dataclass
class AdditionalDescriptor(DMAModelDiff):
    severity = SEVERITY_HIGH
    mmio_address: int
    ram_addresses: List[int]

    def __str__(self) -> str:
        return f"Additional MMIO Register: {self.mmio_address:#x} -> {','.join([hex(addr) for addr in self.ram_addresses])}"

def extract_buf_definitions_from_groundtruth(groundtruth_yaml_path: Path, searchdir: Path = None) -> Dict[Path, List[SimpleDMABuf]]:
    """ Given the path of a ground_truth.yaml file, parse
    the DMA buffers and find the target directory for each entry.

    We need that path to be able to re-use the same functionality as
    for the reference config yamls (config_generic_dma_manual.yml)
    """
    groundtruth_map = load_config_deep(groundtruth_yaml_path)
    groundtruth_parent_dir = groundtruth_yaml_path.parent

    """
    MK64F:
        name: MK64F
        ELF: uart_example.elf  
        buf0:
            type: r
            buffer_address: 0x1fff0078
            buffer_size: 8
            pc_dma_access: {0x8dc}
            bb_dma_access: {0x8cc}

    sample1:
        name: F103_ADC_SingleConversion_TriggerTimer_DMA
        board: f103
        ELF: F103_ADC_SingleConversion_TriggerTimer_DMA.elf
        dma_mmio_base_address: 0x40020000
        buf0:
            type: r
            bb_dma_init: 0x0800026c
            buffer_address: 0x200000a4
            buffer_size: 0x100
            pc_dma_access: {0x08000658, 0x0800069c}
            bb_dma_access: {0x08000658, 0x0800069c}
    """
    res = {}

    # The keys of each entry are arbitrary, so ignore those
    for entry in groundtruth_map.values():
        name = entry['name']
        # We rely on the convention of the 'name' entry matching the target directory name
        # We search for this name in the subdirectories of the directory that the
        # ground_truth.yml resides in.

        if searchdir:
            target_directory_iterator = searchdir.rglob(name+os.sep)
        else:
            target_directory_iterator = groundtruth_parent_dir.rglob(name+os.sep)
        target_directory = next(target_directory_iterator, None)
        if target_directory is None:
            print(f"[ERROR] Could not find any target directory for name '{name}' for ground truth yaml: {groundtruth_yaml_path}")
            exit(1)
        ambiguous_directory = next(target_directory_iterator, None)
        if ambiguous_directory is not None:
            print(f"[ERROR] Ground truth yaml 'name' entry leads to ambiguous target directories: Name '{name}' in {groundtruth_yaml_path} could refer to either\na) '{target_directory}'\nb){ambiguous_directory}\nexiting...")
            exit(1)

        bufs = [
            SimpleDMABuf(
                PLACEHOLDER_MMIO_ADDRESS,
                {
                    buf_entry['buffer_address']: SizeRange(buf_entry['buffer_size'], buf_entry['buffer_size'])
                }
            )
            for buf_name, buf_entry in entry.items() if buf_name.startswith('buf') and buf_entry['type'] == 'r' and ( buf_entry.get("bb_dma_access", None) or buf_entry.get("pc_dma_access", None) )
        ]

        res[target_directory] = bufs

    return res

def scan_for_groundtruth_yamls(groundtruth_root: Path, searchdir: Path = None) -> Dict[Path, List[SimpleDMABuf]]:
    res = {}

    res = {}
    for parent, dirs, files in os.walk(groundtruth_root, topdown=True):
        dirname = os.path.basename(parent)
        if dirname in INVALID_DIRNAMES:
            dirs.clear()
            continue
        if GROUNDTRUTH_YAML_FILENAME not in files:
            continue

        parent = Path(parent)
        groundtruth_path = parent / GROUNDTRUTH_YAML_FILENAME
        assert groundtruth_path.is_file()
        print(f"Found groundtruth file: {groundtruth_path}")

        # Here, unlike for the reference configs, we are not in the target directory
        # We need to figure out the target directory from the 'name' entry of each sample
        res.update(extract_buf_definitions_from_groundtruth(groundtruth_path, searchdir))

    return res

def scan_for_reference_configs_yaml(groundtruth_root: Path) -> Dict[Path, List[SimpleDMABuf]]:
    """Generates a mapping from target name to path of reference model
    
    This can then be used to match ground truth files via project paths.
    """

    res = {}
    for target_parent, dirs, files in os.walk(groundtruth_root, topdown=True):
        dirname = os.path.basename(target_parent)
        if dirname in INVALID_DIRNAMES:
            dirs.clear()
            continue
        if REFERENCE_MODEL_FILENAME not in files or dirname == nc.SESS_DIRNAME_NECESSARY_FILES or dirname == "deprecated":
            continue

        target_parent = Path(target_parent)
        reference_model_path = target_parent / REFERENCE_MODEL_FILENAME
        print(f"Found reference config: {reference_model_path}")
        assert reference_model_path.is_file()
        res[target_parent] = extract_buf_definitions_from_config(load_config_deep(reference_model_path))

    return res

def collect_buffer_addrs_for_descr(descr: dict, buf_addrs: set, buf_sizes: dict):
    if logger.level >= logging.DEBUG:
        print(f"[collect_buffer_addrs_for_descr] Visiting descr: {descr}")
    t = descr.get('type', None)
    if t is None:
        if 'to' in descr:
            t = 'pointer'
        elif 'fields' in descr:
            t = 'descriptor'
    if not t:
        return
    elif t == 'buffer':
        buffer_local_known_sizes = descr.get('known_sizes', {})
        for addr, entry in buffer_local_known_sizes.items():
            buf_sizes[addr] = SizeRange(entry.get("min", entry.get("min_size", 1)), entry.get("max", entry.get("max_size", 0xffffffff)))
    elif t == 'pointer':
        child = descr.get('to', None)
        if child is not None:
            if child.get('type', None) == 'buffer':
                addrs = descr.get("known_values", [])
                if logger.level >= logging.DEBUG:
                    print(f"Found {len(addrs)} new known_values: " + ", ".join([hex(addr) if type(addr) == int else addr for addr in addrs]))
                buf_addrs.update(addrs)
            collect_buffer_addrs_for_descr(child, buf_addrs, buf_sizes)
    elif t == 'descriptor':
        children = descr.get('fields', None)
        if children is not None:
            for child in children:
                if child.get('type', None) == 'buffer':
                    addrs = descr.get("known_values", [])
                    buf_addrs.update(addrs)
                collect_buffer_addrs_for_descr(child, buf_addrs, buf_sizes)

def extract_buf_definitions_from_config(model: dict) -> List[SimpleDMABuf]:
    if not model:
        return []

    res = []

    peripherals: dict = model.get('peripherals', {})
    if not len(peripherals) == 1:
        print(f"[ERROR] found not exactly one peripheral in model: {model}")
        exit(1)

    peripheral = list(peripherals.values())[0]
    # print(peripheral)
    symbols, _ = parse_symbols(model)

    descriptors = peripheral.get('descriptors', {})
    if descriptors:
        known_sizes: Dict[int, SizeRange] = {
            parse_address_value(symbols, ram_addr): SizeRange(entry.get("min", entry.get("min_size", 1)), entry.get("max", entry.get("max_size", 0xffffffff))) for ram_addr, entry in peripheral.get('known_sizes', {}).items()
        }
        if logger.level >= logging.DEBUG:
            print(f"Got {len(known_sizes)} known_sizes:")
            for i, (ram_addr, sizerange)  in enumerate(known_sizes.items(), start=1):
                print(f"{i} {ram_addr:#010x}: {sizerange}")

        for descr in descriptors:
            mmio_addr = parse_address_value(symbols, descr['addr'])
            buf_sizes = {}

            known_ram_addresses = set()
            collect_buffer_addrs_for_descr(descr, known_ram_addresses, buf_sizes)
            known_ram_addresses = [parse_address_value(symbols, v) for v in known_ram_addresses]

            if logger.level >= logging.DEBUG:
                print(f"Collected the following known addresses:" + ", ".join([hex(addr) for addr in known_ram_addresses]))
                print(f"From the following descriptor obj: {descr}")
            if not known_ram_addresses:
                known_ram_addresses = set(known_sizes.keys())
                if logger.level >= logging.DEBUG:
                    print("Found no known addresses, reverting to all known_sizes")

            for addr in known_ram_addresses:
                if addr in buf_sizes:
                    # already found a buffer-local known_sizes entry for this ram addr
                    continue
                if addr not in known_sizes:
                    print(f"[WARNING] No known_size found for known_value address {addr:#x}, using default (grow to infinity)")
                    buf_sizes[addr] = SizeRange()
                else:
                    buf_sizes[addr] = known_sizes[addr]

            res.append(SimpleDMABuf(mmio_addr, buf_sizes))

    legacy_buf_cfg = peripheral.get('buffer', {})
    if legacy_buf_cfg:
        ram_addr = parse_address_value(symbols, legacy_buf_cfg['base']['addr'])

        res.append(SimpleDMABuf (
            peripheral.get('base_addr', PLACEHOLDER_MMIO_ADDRESS),
            {
                ram_addr: SizeRange(legacy_buf_cfg['size']['val'])
            }
        ))

    return res

def generate_diffs(models: List[SimpleDMABuf], other_models: List[SimpleDMABuf]) -> List[DMAModelDiff]:
    res = []

    # buf_by_mmio_addr = {buf.mmio_addr: buf for buf in models}
    buf_by_mmio_addr = {buf.mmio_addr: buf for buf in models}
    buf_by_ram_addr = {ram_addr: buf for buf in models for ram_addr in buf.known_sizes}
    other_buf_by_mmio_addr = {buf.mmio_addr: buf for buf in other_models}
    other_buf_by_ram_addr = {ram_addr: buf for buf in other_models for ram_addr in buf.known_sizes}

    if logger.level >= logging.DEBUG:
        print("===== generate_diffs =====")
        print("own_buf_by_mmio_addr", buf_by_mmio_addr)
        print("other_buf_by_mmio_addr", other_buf_by_mmio_addr)
        print("own_buf_by_ram_addr", buf_by_ram_addr)
        print("other_buf_by_ram_addr", other_buf_by_ram_addr)
        print("==========================")

    mismatching_mmio_addr_buf_addr_pairs = set()

    # Detect differences
    for buf in models:
        other_buf = other_buf_by_mmio_addr.get(buf.mmio_addr, None)
        if logger.level >= logging.DEBUG:
            print(f"Diffing {buf} vs. {other_buf}")
        
        if not other_buf:
            # No Buffer for the MMIO address

            # Same Buffer RAM address for other MMIO address?
            other_bufs_for_same_ram_addr = [other_buf_by_ram_addr[ram_addr] for ram_addr in buf.known_sizes if ram_addr in other_buf_by_ram_addr]
            if not other_bufs_for_same_ram_addr:
                # No buffer for same RAM address
                res.append(AdditionalDescriptor(buf.mmio_addr, list(buf.known_sizes.keys())))
                continue
            else:
                # Same RAM buffer, but other MMIO register
                for other_buf in other_bufs_for_same_ram_addr:
                    res.append(DifferentMMIOReg(buf.mmio_addr, other_buf.mmio_addr))
                    for ram_address in other_buf.known_sizes:
                        mismatching_mmio_addr_buf_addr_pairs.add((other_buf.mmio_addr, ram_address))

                if len(other_bufs_for_same_ram_addr) == 1 and other_bufs_for_same_ram_addr[0].mmio_addr == PLACEHOLDER_MMIO_ADDRESS:
                    other_buf = other_bufs_for_same_ram_addr[0]
                else:
                    continue

        own_ram_addresses_not_in_other = set()
        other_ram_addresses_not_in_own = set()
        ram_addresses_in_both = set()

        # We have another buffer
        for ram_address, sizerange in buf.known_sizes.items():
            # 1. Compare RAM addresses
            other_sizerange = other_buf.known_sizes.get(ram_address, None)

            if not other_sizerange:
                own_ram_addresses_not_in_other.add(ram_address)
                continue
            else:
                ram_addresses_in_both.add(ram_address)

            # 2. Compare buffer sizes
            if sizerange != other_sizerange:
                res.append(DifferentSize(buf.mmio_addr, ram_address, sizerange, other_sizerange))
                continue

        for ram_address in other_buf.known_sizes:
            if ram_address not in buf.known_sizes:
                other_ram_addresses_not_in_own.add(ram_address)

        if other_ram_addresses_not_in_own:
            # We are missing RAM addresses in this descriptor
            if own_ram_addresses_not_in_other:
                # We also have additional ones, they are just different
                res.append(DifferentBufferAddresses(buf.mmio_addr, sorted(own_ram_addresses_not_in_other), sorted(other_ram_addresses_not_in_own)))
            else:
                # We have no additional ones, we are flat missing some
                res.append(MissingBufferAddresses(buf.mmio_addr, sorted(other_ram_addresses_not_in_own)))
        elif own_ram_addresses_not_in_other:
            # We have additional ones, but are missing none
            res.append(AdditionalBufferAddresses(buf.mmio_addr, sorted(own_ram_addresses_not_in_other)))

    for other_buf in other_models:
        if logger.level >= logging.DEBUG:
            print(f"Looking at other buf: {other_buf} to check for missing descriptors")

        # For the other side, check for missing MMIO addresses only
        is_mmio_addr_missing = other_buf.mmio_addr not in buf_by_mmio_addr
        is_already_marked_as_different_mmio_reg = all((((other_buf.mmio_addr, ram_address) in mismatching_mmio_addr_buf_addr_pairs) for ram_address in other_buf.known_sizes))
        if is_mmio_addr_missing and not is_already_marked_as_different_mmio_reg:
            res.append(MissingDescriptor(other_buf.mmio_addr, list(other_buf.known_sizes.keys())))
            continue

    return res

def get_model_path(projdir: str, snipdir_postfix) -> str:
    if not snipdir_postfix:
        # For default model, use the one in the projdir
        return os.path.join(projdir, nc.PIPELINE_FILENAME_DMA_CFG)
    else:
        snipdir_path = nc.dma_snippet_path_for_proj(projdir, snipdir_postfix)
        return os.path.join(snipdir_path, nc.SESS_DIRNAME_DMA_CFG_CANDIDATES, nc.PIPELINE_FILENAME_DMA_CFG)

def get_reference_model(projdir: str, reference_snipdir_postfix: str | None, groundtruth_snippets: Dict[Path, List[SimpleDMABuf]]) -> List[SimpleDMABuf]:
    reference_bufs = None

    if reference_snipdir_postfix is not None:
        # Resolve via reference snipdir postfix
        reference_model_path = get_model_path(projdir, reference_snipdir_postfix)
        if logger.level >= logging.DEBUG:
            print(f"Loading reference model immediately from {reference_model_path}")
        reference_model = load_config_deep(reference_model_path)
        reference_bufs = extract_buf_definitions_from_config(reference_model)
    else:
        # Try to match groundtruth snippet via project path
        # We cannot simply go with the target name, as it repeats
        # Thus, we filter for matching target directory names
        # and then count the number of overlaps in parent directory names to find the correct candidate
        # This allows us to differentiate, e.g.: serial-contiguous from serial-scatter-gather

        proj_path = Path(projdir).resolve()
        proj_path_dirnames = [p.name for p in proj_path.parents]

        overlap_counts = {}
        for target_dir_path in groundtruth_snippets:
            if target_dir_path.name in proj_path_dirnames:
                count = 1
                for target_dir_parent in target_dir_path.parents:
                    if target_dir_parent.name in proj_path_dirnames:
                        count += 1
                overlap_counts[target_dir_path] = count
        if overlap_counts:    
            reference_target_dir_path, max_count = max(overlap_counts.items(), key=lambda e: e[1])
            if max_count != 0:
                reference_bufs = groundtruth_snippets[reference_target_dir_path]
                if logger.level >= logging.DEBUG:
                    print(f"Looked up reference model for {reference_target_dir_path}: {reference_bufs}")

    return reference_bufs

def diff_project_models(projdirs: List[str], snipdir_postfix: str, reference_snipdir_postfix: str | None, groundtruth_models: Dict[str, List[SimpleDMABuf]]) -> Dict[str, List[DMAModelDiff]]:
    # Consistency check
    assert reference_snipdir_postfix is None or not groundtruth_models
    projects_without_diffs = []
    excluded_projects = []

    diffs_by_projdir = {}
    diffs_by_type = {}
    for projdir in projdirs:
        snipdir_path = nc.dma_snippet_path_for_proj(projdir, snipdir_postfix)
        if not os.path.exists(snipdir_path):
            print(f"[WARNING] DMA models have not been (re-)generated in project. Expected snippet path: {snipdir_path}")
            excluded_projects.append(projdir)
            continue
        perf_metadata_path = os.path.join(snipdir_path, nc.SESS_DIRNAME_DMA_CFG_CANDIDATES, nc.PIPELINE_FILENAME_DMA_MODEL_PERF_METADATA)
        if snipdir_postfix and not os.path.exists(perf_metadata_path):
            print(f"[WARNING] Performance metadata not available, modeling seems to be still running. Expected metadata path: {perf_metadata_path}")
            excluded_projects.append(projdir)
            continue

        model_path = get_model_path(projdir, snipdir_postfix)
        model = load_config_deep(model_path)

        reference_bufs: List[SimpleDMABuf] = get_reference_model(projdir, reference_snipdir_postfix, groundtruth_models)
        if reference_bufs is None:
            print(f"[WARNING] No groundtruth model available. Skipping snippet path: {snipdir_path}")
            continue

        if logger.level >= logging.DEBUG:
            print(f"Loaded reference models for '{snipdir_path}':\n{reference_bufs}\n --------------------")

        bufs = extract_buf_definitions_from_config(model)
        diffs = [diff for diff in generate_diffs(bufs, reference_bufs) if not (type(diff) == DifferentMMIOReg and diff.other_mmio_addr == PLACEHOLDER_MMIO_ADDRESS)]
        if diffs:
            diffs_by_projdir[projdir] = diffs
            for diff in diffs:
                diffs_by_type.setdefault(type(diff), {}).setdefault(projdir, []).append(diff)
        else:
            projects_without_diffs.append(projdir)

    return diffs_by_projdir, diffs_by_type, projects_without_diffs, excluded_projects

def diff_project_modeling_perf(projdirs: List[str], snipdir_postfix: str, reference_snipdir_postfix: str) -> Tuple[DMAJobPerfSummary, DMAJobPerfSummary, Dict[str, Tuple[DMAJobPerfSummary, DMAJobPerfSummary]]]:
    # 1. absolute numbers
    # 2. numbers relative to trace generation timings

    if not snipdir_postfix:
        print("[ERROR] Getting performance metrics for the default pipeline-generated models is not supported")
        exit(1)

    if not reference_snipdir_postfix:
        print("[WARNING] Did not get passed a reference, just showing performance numbers")
        reference_snipdir_postfix = snipdir_postfix

    summaries_per_project = {}
    summaries = []
    reference_summaries = []
    missing_perf_data, missing_reference_perf_data = False, False
    for projdir in projdirs:
        snipdir_path = nc.dma_snippet_path_for_proj(projdir, snipdir_postfix)
        reference_snipdir_path = nc.dma_snippet_path_for_proj(projdir, reference_snipdir_postfix)

        perf_metadata_path = os.path.join(snipdir_path, nc.SESS_DIRNAME_DMA_CFG_CANDIDATES, nc.PIPELINE_FILENAME_DMA_MODEL_PERF_METADATA)
        reference_perf_metadata_path = os.path.join(reference_snipdir_path, nc.SESS_DIRNAME_DMA_CFG_CANDIDATES, nc.PIPELINE_FILENAME_DMA_MODEL_PERF_METADATA)
        if not os.path.exists(reference_perf_metadata_path):
            missing_reference_perf_data = True
            print(f"[WARNING] Performance metadata not found for projdir {projdir} (reference), skipping")
            continue
        if not os.path.exists(perf_metadata_path):
            missing_perf_data = True
            print(f"[WARNING] Performance metadata not found for projdir {projdir}, skipping")
            continue

        perf_metadata: List[Tuple[str, DMAJobPerfResult]] = eval_utils.parse_dma_perf_metadata(perf_metadata_path)
        reference_perf_metadata: List[Tuple[str, DMAJobPerfResult]] = eval_utils.parse_dma_perf_metadata(reference_perf_metadata_path)

        perf_summary: DMAJobPerfSummary = eval_utils.summarize_dma_perf_metadata(perf_metadata, snipdir_path)
        reference_perf_summary: DMAJobPerfSummary = eval_utils.summarize_dma_perf_metadata(reference_perf_metadata, reference_snipdir_path)

        summaries_per_project[projdir] = (perf_summary, reference_perf_summary)
        summaries.append(perf_summary)
        reference_summaries.append(reference_perf_summary)

    if not summaries_per_project:
        print(f"[ERROR] Could not find any performance metadata. New missing/Reference missing: {missing_perf_data}/{missing_reference_perf_data} (snipdir postfixes: '{snipdir_postfix}', '{reference_snipdir_postfix}')")
        exit(1)

    overall_perf_summary = eval_utils.summarize_dma_perf_metadata_summaries(summaries)
    overall_reference_perf_summary = eval_utils.summarize_dma_perf_metadata_summaries(reference_summaries)

    return overall_perf_summary, overall_reference_perf_summary, summaries_per_project

def model_diff_main(args):
    projdirs: List[str] = []
    print(args)
    for root_dir in args.root:
        projdirs.extend(find_proj.find_projdirs(root_dir))
    
    if not projdirs:
        print("Found no project directories. Nothing to do...")
        exit(1)

    if args.name:
        snipdir_postfix = "_" + args.name
    else:
        snipdir_postfix = ""

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.ref_name:
        if args.groundtruth_root is not None:
            print("[ERROR] Cannot specify reference model name and a groundtruth root at the same time. You can diff only either against a ground truth, or against another modeling.")
            exit(1)
        reference_snipdir_postfix = "_" + args.ref_name
    else:
        reference_snipdir_postfix = ""

    num_procs = args.num_cores
    if num_procs != 1:
        print("[WARNING] Multi-processed diffing is currently not supported, ignoring...")

    if not args.perf:
        groundtruth_models = None
        if args.groundtruth_root:
            if not args.groundtruth_root.is_dir():
                print(f"[ERROR] Ground truth root must be a directory: {args.groundtruth_root}")
                exit(1)
            args.groundtruth_root = args.groundtruth_root.resolve()
            reference_snipdir_postfix = None

            if args.groundtruth_type == GROUNDTRUTH_TYPE_REFERENCE_CONFIG:
                groundtruth_models = scan_for_reference_configs_yaml(args.groundtruth_root)
            elif args.groundtruth_type == GROUNDTRUTH_TYPE_GROUNDTRUTH_YAML:
                if args.searchdir:
                    groundtruth_models = scan_for_groundtruth_yamls(args.groundtruth_root, args.searchdir)
                else:
                    groundtruth_models = scan_for_groundtruth_yamls(args.groundtruth_root)
            else:
                assert False, "Unknown groundtruth type"

        #  
        diffs_by_project, diffs_by_type, projects_without_diff, skipped_projects = diff_project_models(projdirs, snipdir_postfix, reference_snipdir_postfix, groundtruth_models)
        import yaml
        res = {}
        res["diffs_by_project"] = diffs_by_project
        res["projects_without_diff"] = projects_without_diff 
        res["skipped_projects"] = skipped_projects 

        with open("results-01.yml","w") as f:
            f.write(yaml.dump(res, allow_unicode=True, default_flow_style=False))
        # print(diffs_by_project)

        if not diffs_by_project:
            if not projects_without_diff:
                print("Did not find any projects that matched...")
            else:
                print(f"No differences in {len(projects_without_diff)} projects (#skipped: {len(skipped_projects)})).")
                print("\n".join(projects_without_diff))
                print("\t-> All good :-)")
        else:
            if args.file:
                with open(args.file,"w") as outfile:
                    yaml.dump(diffs_by_project,outfile)
            num_diffs = sum((len(diffs) for diffs in diffs_by_project.values()))
            print(f"Got {num_diffs} diffs across {len(diffs_by_project)} projects (#without diff: {len(projects_without_diff)}, #skipped: {len(skipped_projects)})")

            #for projdir, diffs in diffs_by_project.items():
            #    print(f"================== {projdir} ==================")
            #    for diff in diffs:
            #        print(diff)

            for diff_type, projdir_to_diffs in sorted(diffs_by_type.items(), key=lambda e: e[0].severity):
                print(f"\n================== {diff_type.__name__} ==================\n")
                for projdir, diffs in sorted(projdir_to_diffs.items(), key=lambda e: e[0]):
                    print(f"================== {projdir} ==================")
                    for diff in diffs:
                        print(diff)
    else:
        # Compare performance metrics instead of models
        overall_perf_summary, overall_reference_perf_summary, summaries_per_project = diff_project_modeling_perf(projdirs, snipdir_postfix, reference_snipdir_postfix)

        if args.verbose:
            for projdir, (perf_summary, reference_perf_summary) in summaries_per_project.items():
                print(f"Project: {projdir}")
                print(f"Perf summary            : {perf_summary}")
                print(f"Perf summary (reference): {reference_perf_summary}")

            print("Overall stats")
            print(overall_perf_summary)
            print(overall_reference_perf_summary)

        try:
            factor = overall_perf_summary.time_dma_snippet_gen / overall_perf_summary.time_trace_gen
            reference_factor = overall_reference_perf_summary.time_dma_snippet_gen / overall_reference_perf_summary.time_trace_gen
            max_factor = overall_perf_summary.max_factor_trace_gen_to_dma_snip_gen
            max_reference_factor = overall_reference_perf_summary.max_factor_trace_gen_to_dma_snip_gen

            speedup_avg = round(reference_factor / factor, 4) if factor != 0 else "inf"
            speedup_max = round(max_reference_factor / max_factor, 4) if max_factor != 0 else "inf"

            print("========================")
            print(f"Factors between trace gen and snippet gen (avg). {round(factor, 2)} vs. {round(reference_factor, 2)} (speedup: {speedup_avg})")
            print(f"Factors between trace gen and snippet gen (max). {round(max_factor, 2)} vs. {round(max_reference_factor, 2)} (speedup: {speedup_max})")
            print(f"Max factor path (new): {overall_perf_summary.path_max_factor_trace_gen_to_dma_snip_gen}")
            print(f"Max factor path (ref): {overall_reference_perf_summary.path_max_factor_trace_gen_to_dma_snip_gen}")
        except ZeroDivisionError:
            print("[ERROR] Division by zero error. We seem to be dealing with negligible timings...")
            import traceback 
            print(f"Original error:\n{traceback.format_exc()}")
