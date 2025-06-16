from dataclasses import dataclass
from diffing import GROUNDTRUTH_YAML_FILENAME, SEVERITY_LOW, SEVERITY_MEDIUM, SEVERITY_HIGH
from pathlib import Path
import os
from typing import List, Tuple, Dict
from fuzzware_harness.util import load_config_deep, parse_address_value, parse_symbols
from enum import Enum

GROUNDTRUTH_DICE_YAML_FILENAME = "ground_truth_dice_perspective.yml"

def add_groundtruth_diff_parsing(common_parser, sub_parsers):
    parser = sub_parsers.add_parser("diff-groundtruths", help="Diff one ground truth YAML file with another", add_help=False, parents=[common_parser])
    parser.set_defaults(func=groundtruth_diff_main)

    parser.add_argument('--root', type=Path, required=True, help=f"Base directory to find groundtruth files in. Searches for neighbouring files of names specified via '--groundtruth-name' and '--reference-groundtruth-name' (default: {GROUNDTRUTH_DICE_YAML_FILENAME} and {GROUNDTRUTH_YAML_FILENAME})")
    parser.add_argument('--groundtruth-name', type=str, default=GROUNDTRUTH_DICE_YAML_FILENAME, help=f"Name of the groundtruth file that is evaluated. Default: {GROUNDTRUTH_DICE_YAML_FILENAME}")
    parser.add_argument('--reference-groundtruth-name', type=str, default=GROUNDTRUTH_YAML_FILENAME, help=f"Name of the reference groundtruth file to compare against. Default: {GROUNDTRUTH_YAML_FILENAME}")

def scan_for_groundtruth_yamls(root: Path, filename: str, reference_filename: str) -> List[Tuple[dict, dict]]:
    res = []

    for parent, dirs, files in os.walk(root):
        if not (filename in files and reference_filename in files):
            if filename in files:
                print(f"[WARNING] Skipping: found groundtruth file {filename}, but not its reference {reference_filename} in '{parent}'.")
            elif reference_filename in files:
                print(f"[WARNING] Skipping: found reference groundtruth file {reference_filename}, but no to-be-diffed {filename} in '{parent}'")
            continue

        parent = Path(parent)
        groundtruth_path = parent / filename
        assert groundtruth_path.is_file()
        reference_groundtruth_path = parent / reference_filename
        print(f"Found groundtruth file: {groundtruth_path}")
        print(f"Found reference groundtruth file: {reference_groundtruth_path}")

        # Here, unlike for the reference configs, we are not in the target directory
        # We need to figure out the target directory from the 'name' entry of each sample
        res.append(
            (load_config_deep(groundtruth_path),
            load_config_deep(reference_groundtruth_path))
        )

    return res

class GroundTruthDiff:
    severity: int = 0

@dataclass
class DifferentBufferType(GroundTruthDiff):
    severity = SEVERITY_MEDIUM
    detected_buf: 'GroundTruthBuffer'
    expected_buf: 'GroundTruthBuffer'

    def __str__(self) -> str:
        return f"Different type for {self.detected_buf.address:#x}. Expected: {self.expected_buf.type.name}, got: {self.detected_buf.type.name} (Got buf: {self.detected_buf}, expected buf: {self.expected_buf})"

@dataclass
class MissingBuffer(GroundTruthDiff):
    severity = SEVERITY_MEDIUM
    buf: 'GroundTruthBuffer'

    def __str__(self) -> str:
        return f"Missing buffer: {self.buf}."

@dataclass
class AdditionalBuffer(GroundTruthDiff):
    severity = SEVERITY_MEDIUM
    buf: 'GroundTruthBuffer'

    def __str__(self) -> str:
        return f"Additional, unexpected buffer: {self.buf}"

@dataclass
class ShadowedTXMisclassification(GroundTruthDiff):
    severity = SEVERITY_LOW
    reference_buf: 'GroundTruthBuffer'
    config_reached: bool

    def __str__(self) -> str:
        return f"Shadowed access to TX buffer: {self.reference_buf} (config reached? {self.config_reached})"

@dataclass
class CorrectClassification(GroundTruthDiff):
    severity = SEVERITY_LOW 
    detected_buf: 'GroundTruthBuffer'
    expected_buf: 'GroundTruthBuffer'
    
    def __str__(self) -> str:
        return f"Correct classification. Detected type {self.detected_buf.type.name} matches expected type {self.expected_buf.type.name}. Detected buf {self.detected_buf} matches expected buf {self.expected_buf})"

#dataclass
class CorrectDummy(GroundTruthDiff):
    severity = SEVERITY_LOW
    
    def __str__(self) -> str:
        return f"Correct classification. Nothing to report."


class GroundTruthBufferType(Enum):
    RX = "r"
    TX = "t"

@dataclass
class GroundTruthBuffer:
    type: GroundTruthBufferType # BUFFER_TYPE_RX | BUFFER_TYPE_TX
    address: int
    mmio_dma_ptr: int | None | List[int]
    size: int
    access_addrs: List[int]

    def __str__(self) -> str:
        return f"[{self.address:#x}] {self.type.name} size {self.size} (mmio addr: {hex(self.mmio_dma_ptr) if type(self.mmio_dma_ptr) == int else self.mmio_dma_ptr})"

@dataclass
class GroundTruthSample:
    name: str | None
    # board: str | None
    # elf: str | None
    # peripheral_mmio_base_addr
    bufs: List[GroundTruthBuffer]

    @staticmethod
    def deserialize(entry: dict) -> 'GroundTruthSample':
        bufs = []
        for name, buf_def in entry.items():
            if not name.startswith("buf"):
                continue
            bufs.append(GroundTruthBuffer(
                type=GroundTruthBufferType(buf_def["type"]),
                address=buf_def["buffer_address"],
                mmio_dma_ptr=buf_def.get("mmio_dma_ptr"),
                size = buf_def['buffer_size'],
                access_addrs = list(buf_def.get("pc_dma_access", [])) + list(buf_def.get("bb_dma_access", []))
            ))

        return GroundTruthSample(
            entry.get("name"),
            bufs,
        )

    def diff(self, other: 'GroundTruthSample') -> List[GroundTruthDiff]:
        """Diff the DMA buffers for two ground-truth files. This is mainly used to
        diff the DICE-assumed ground truth against the actual ground truth of the
        DICE unit test sample set.

        Different situations:
        # <dice-buffer-type> vs. <groundtruth-buffer-type> -> <Implication>
        none  vs.    none -> All good
        rx    vs.    rx   -> All good
        tx    vs.    tx   ->
            a) Firmware never accesses buffer -> All good
            b) Firmware would access buffer   -> DICE rx/tx identification issue shadowed by fuzzer limitation

        rx    vs.    tx   -> DICE rx/tx detection issue (firmware accesses TX buffer)
        tx    vs.    rx   ->
            a) Firmware never accesses buffer -> All good
            b) Otherwise, likely a fuzzer Limitation: fuzzer never reaches access to buffer

        none  vs.    rx   ->
            a) MMIO register layout DICE-conform: Likely a fuzzer Limitation: fuzzer never reaches config of buffer
            b) MMIO register layout not DICE-conform: DICE detection limitation (or Shadowing by fuzzer limitation)
        none  vs.    tx   ->
            a) MMIO register layout DICE-conform
                a.1) Firmware never accesses TX buffer: Likely a fuzzer Limitation: fuzzer never reaches config of buffer
                a.2) Firmware would access TX buffer: DICE rx/tx identification issue shadowed by fuzzer limitation
            b) MMIO register layout not DICE-conform: DICE rx/tx identification issue shadowed by fuzzer limitation
        rx    vs.    none -> DICE Mis-classification: Write of pointer-like pair to MMIO registers
        tx    vs.    none -> DICE Mis-classification: Write of pointer-like pair to MMIO registers
        """
        res = []

        # Collect buffers
        bufs_by_ram_addr: Dict[int, List[GroundTruthBuffer]] = {}
        for buf in self.bufs:
            bufs_by_ram_addr.setdefault(buf.address, []).append(buf)

        reference_bufs_by_ram_addr: Dict[int, List[GroundTruthBuffer]] = {}
        for buf in other.bufs:
            reference_bufs_by_ram_addr.setdefault(buf.address, []).append(buf)

        # Sort (to make matching easier for comparisons involving multiple buffers for the same RAM address)
        for bufs in bufs_by_ram_addr.values():
            bufs.sort(key=lambda buf: buf.type.value)
        for bufs in reference_bufs_by_ram_addr.values():
            bufs.sort(key=lambda buf: buf.type.value)

        # Diff buffers
        for buf_addr, bufs in bufs_by_ram_addr.items():
            other_bufs = reference_bufs_by_ram_addr.get(buf_addr, [])

            if not other_bufs:
                res.append(AdditionalBuffer(buf=buf))
                continue

            # We got at least one buffer at the address in the ground truth
            for i, buf in enumerate(bufs):
                if len(other_bufs) <= i:
                    # If we have multiple buffers for the same address (re-use),
                    # then only point out RX buffers (to avoid reporting re-use)
                    if buf.type == GroundTruthBufferType.RX:
                        res.append(AdditionalBuffer(buf=buf))
                    continue
                other_buf = other_bufs[i]
                if buf.type != other_buf.type:
                    # Okay case: There is no access to the buffer at all, so RX not relevant
                    # (minus edge cases where this is followed by Mem-2-Mem or Mem-2-Peripheral transfer)
                    if other_buf.type == GroundTruthBufferType.RX and not other_buf.access_addrs:
                        continue
                    res.append(DifferentBufferType(detected_buf=buf, expected_buf=other_buf))
                elif buf.type == GroundTruthBufferType.TX and other_buf.access_addrs:
                    res.append(ShadowedTXMisclassification(reference_buf=other_buf, config_reached=True))

        for buf_addr, reference_bufs in reference_bufs_by_ram_addr.items():
            own_bufs = bufs_by_ram_addr.get(buf_addr, [])
            for other_buf in reference_bufs[len(own_bufs):]:
                if other_buf.type == GroundTruthBufferType.TX and other_buf.access_addrs:
                    res.append(ShadowedTXMisclassification(reference_buf=other_buf, config_reached=False))
                else:
                    res.append(MissingBuffer(buf=other_buf))

        return res

def diff_sample_entries(sample_dict, reference_sample_dict) -> List[GroundTruthDiff]:
    
    sample = GroundTruthSample.deserialize(sample_dict)
    reference_sample = GroundTruthSample.deserialize(reference_sample_dict)
    
    return sample.diff(reference_sample)

def groundtruth_diff_main(args):
    groundtruth_pairs: List[Tuple[dict, dict]] = scan_for_groundtruth_yamls(args.root, args.groundtruth_name, args.reference_groundtruth_name)
    skipped_samples = set()

    print(f"Found groundtruth pairs: {groundtruth_pairs}")

    diffs_by_sample = {}
    for groundtruth, reference_groundtruth in groundtruth_pairs:
        for sample_name, sample in groundtruth.items():
            reference_sample = reference_groundtruth.get(sample_name, None)
            if reference_sample is None:
                print(f"[WARNING] Found extra sample {sample_name} that is not present in the reference ground truth. Skipping...")
                assert sample_name not in skipped_samples, "We have a collision in missing"
                skipped_samples.add(sample_name)
                continue
            
            diffs = diff_sample_entries(sample, reference_sample)
            if diffs:
                diffs_by_sample[(sample_name, reference_sample.get("name", "<UNKN>"))] = diffs

    diffs_by_type = {}
    for (sample_id, name), diffs in diffs_by_sample.items():
        for diff in diffs:
            diffs_by_type.setdefault(type(diff), []).append((name, diff))

    print(f"Got {sum(len(diffs) for diffs in diffs_by_sample.values())} diffs for {sum((len(samples[0]) for samples in groundtruth_pairs))} sample pairs:")
    #for (sample_id, name), diffs in diffs_by_sample.items():
    #    print(f"==== {sample_id}: {name} ===")
    #    for diff in diffs:
    #        print(diff)
            
    for diff_type, name_and_diff_pairs in sorted(diffs_by_type.items(), key=lambda e: e[0].severity):
        print(f"\n====== {diff_type.__name__} ======")
        max_len = max((len(name) for name, diff in name_and_diff_pairs))
        for name, diff in name_and_diff_pairs:
            print(f"{name.ljust(max_len+1)}: {diff}")
