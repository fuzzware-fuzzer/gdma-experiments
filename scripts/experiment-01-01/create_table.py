import yaml
import argparse
from pathlib import Path
from dataclasses import dataclass
import sys
from texttable import Texttable
import latextable
import diffing
import groundtruthdiffing

from typing import Tuple, Dict, List

# 1: correct
# 2: size wrong (can only appear for fuzzware)
# 3: missing descriptor (we only award missing descriptor if rx is missing, a missing tx is ignored for now)
# 4: wrong buffer classification (gt tx, detected rx)
# 5: fuzzer limitation (gt rx, detected tx) 
CASE_1=1
CASE_2=2
CASE_3=3
CASE_4=4
CASE_5=5
CASE_6=6


# number of samples
NUM_SAMPLES = 33

FUZZWARE_LIMITATIONS = ["NRF51822_console_bleprph", "NRF52832_console_bleprph"]
# if we have a dma stream configuration but no access in dice, we assume a fuzzer limitation
# F103_USART_SyncCommunication_FullDuplex_DMA has both a fuzzer limitation and a wrong mechanism. We put it in the wrong mechanism categoty
P2IM_LIMITATIONS = ["F103_ChibiOS_acelerometer", "F103_I2C_TwoBoards_MasterTx_SlaveRx_DMA", "F103_UART_HyperTerminal_DMA", "F103_UART_TwoBoards_ComDMA", "F429_ChibiOS_ADC_slider", "NUC123_PDMA_memory", "NUC123_PDMA_usart", "SAM3X_spi_spi_dmac_slave_example_flash", "SAM3X_usart_dmac_example"]
DICE_UNSUPPORTED = ["NRF51822_SPI_slave", "NRF51822_console_bleprph", "NRF52832_SPI_master", "NRF52832_SPI_slave", "NRF52832_console_bleprph", "NRF52832_uart"]

# take a ground truth yaml-loaded object and return it in a usable way
def parse_ground_truth(data):
    ground_truth = {}
    # parse ground truth
    for value in data.values():
        # we want the name 
        name = value["name"]
        # and the buffers. They are called buf0, buf1,...
        buf_index = 0
        ground_truth[name] = []
        # we don't know the number of buffers
        while True:
            try:
                buf = value[f"buf{buf_index}"]
                mmio = value["dma_mmio_dest_regs"].keys()
                ground_truth[name].append((buf,mmio))
                buf_index+=1
            except:
                # this buffer does not exist anymore, we are done
                break
    return ground_truth

# take a dice yaml-loaded object and return it in a usable way
def parse_dice(dice_data):
    dice_dict = {}
    for value in dice_data.values():
        # we want the name 
        name = value["name"]
        # and the buffers. They are called buf0, buf1,...
        buf_index = 0
        dice_dict[name] = []
        # we don't know the number of buffers
        while True:
            try:
                buf = value[f"buf{buf_index}"]
                dice_dict[name].append(buf)
                buf_index+=1
            except:
                # this buffer does not exist anymore, we are done
                break
    return dice_dict


# take a differentsize type and check if it is equal with loose equality
# loose equality here means that min_size<=actualsize<=max_size
# a different size report is only generated if this is the only difference,
# so no need to check other conditions
def is_equal(diff):
    # detected values
    min_size = diff.size.minsize
    max_size = diff.size.maxsize
    # reference
    other_min = diff.other_size.minsize
    other_max = diff.other_size.maxsize
    if min_size <= other_min and max_size >= other_max:
        return True
    return False

def build_missingbuffer(buf):
    accesses = []
    if "pc_dma_access" in buf.keys():
        accesses += buf["pc_dma_access"]
    if "bb_dma_access" in buf.keys():
        accesses += buf["bb_dma_access"]
    expected_buf = groundtruthdiffing.GroundTruthBuffer(
            type=groundtruthdiffing.GroundTruthBufferType(buf["type"]),
            address=buf["buffer_address"],
            mmio_dma_ptr=None, # we do not know the ground truth pointer
            size=buf["buffer_size"],
            access_addrs = accesses # probably also not very useful down the line
        )
    obj = groundtruthdiffing.MissingBuffer(buf=expected_buf)
    return obj


# parse a gpdma yaml object
# and check if it matches the ground truth
# we can do this here because the data types 
# have ground truth inside
def parse_and_interpret_gpdma(data, ground_truth):
    gpdma_dict = {}
    # we have 3 entries in the dict
    # diffs_by_project, projects_without_diff, skipped_projects
    gpdma_diffs = data["diffs_by_project"]
    for k in gpdma_diffs.keys():
        # we have 5 different runs
        # taking the best one does not seem fair
        # so we always take index 0
        parent_path = Path(k).parent
        if not str(parent_path).endswith("0"):
            continue
        # value is a list of differences
        value = gpdma_diffs[k]
        # we know that the name of the firmware is the name of the grandparent
        name = parent_path.parent.name
        # check the reason we are different
        for diff in value:
            # different size?
            if type(diff) == diffing.DifferentSize:
                gt_buf = ground_truth[name]
                # the diff script reports a different size if we do not have an exact match
                try:
                    tmp = gpdma_dict[name]
                except:
                    gpdma_dict[name] = []
                if is_equal(diff):
                    # we need a dummy because the regular correct needs both buffers,
                    # which we do not know here
                    gpdma_dict[name].append(groundtruthdiffing.CorrectDummy())
                else:
                    gpdma_dict[name].append(diff)
            elif type(diff) == diffing.MissingDescriptor:
                try:
                    tmp = gpdma_dict[name]
                except:
                    gpdma_dict[name] = []
                # we did not find the descriptor
                # not much to do
                gpdma_dict[name].append(diff)
            else:
                sys.err.write(f"Found unmatched diff: {type(diff)}. Please implement.")
                exit(1)
    # a list of projects that did not detect a diff
    gpdma_correct = data["projects_without_diff"]
    for correct in gpdma_correct:
        # again, only take index 0
        parent_path = Path(correct).parent
        if not str(parent_path).endswith("0"):
            continue
        # extract the name
        name = parent_path.parent.name
        # check that the name is not yet covered
        assert name not in gpdma_dict.keys(), f"{name} is a duplicate in results!" 
        try:
            tmp = gpdma_dict[name]
        except:
            gpdma_dict[name] = []
        # no diff, so check
        # dummy needed because we do not know both buffers
        gpdma_dict[name].append(groundtruthdiffing.CorrectDummy())
    # which were skipped?
    gpdma_skipped = data["skipped_projects"]
    for skipped in gpdma_skipped:
        # no idea how this looks like, but we do not have any, so just raise
        # we should assign x if we ever detect one
        assert 0,"Handling of skipped samples not implemented"
    return gpdma_dict



def build_additionalbuffer(buf):
    found_buf = groundtruthdiffing.GroundTruthBuffer(
            type=groundtruthdiffing.GroundTruthBufferType(buf["type"]),
            address=buf["buffer_address"],
            mmio_dma_ptr=buf["mmio_dma_ptr"], # dice has the ptr 
            size=buf["buffer_size"],
            access_addrs = [] # dice does not have it 
        )
    obj = groundtruthdiffing.AdditionalBuffer(buf=found_buf)
    return obj


def build_correctclassification(gt,other):
    accesses = []
    if "pc_dma_access" in gt.keys():
        accesses += gt["pc_dma_access"]
    if "bb_dma_access" in gt.keys():
        accesses += gt["bb_dma_access"]
    expected_buf = groundtruthdiffing.GroundTruthBuffer(
            type=groundtruthdiffing.GroundTruthBufferType(gt["type"]),
            address=gt["buffer_address"],
            mmio_dma_ptr=None, # we do not know the ground truth pointer
            size=gt["buffer_size"],
            access_addrs = accesses # probably also not very useful down the line
        )
    obtained_buf = groundtruthdiffing.GroundTruthBuffer(
            type=groundtruthdiffing.GroundTruthBufferType(other["type"]),
            address=other["buffer_address"],
            mmio_dma_ptr=other["mmio_dma_ptr"], # dice has the ptr 
            size=other["buffer_size"],
            access_addrs = [] # dice does not have it 
        )
    correct = groundtruthdiffing.CorrectClassification(detected_buf=obtained_buf, expected_buf=expected_buf)
    return correct

def build_differentbuffertype(gt,other):
    accesses = []
    if "pc_dma_access" in gt.keys():
        accesses += gt["pc_dma_access"]
    if "bb_dma_access" in gt.keys():
        accesses += gt["bb_dma_access"]
    expected_buf = groundtruthdiffing.GroundTruthBuffer(
            type=groundtruthdiffing.GroundTruthBufferType(gt["type"]),
            address=gt["buffer_address"],
            mmio_dma_ptr=None, # we do not know the ground truth pointer
            size=gt["buffer_size"],
            access_addrs = accesses # probably also not very useful down the line
        )
    obtained_buf = groundtruthdiffing.GroundTruthBuffer(
            type=groundtruthdiffing.GroundTruthBufferType(other["type"]),
            address=other["buffer_address"],
            mmio_dma_ptr=other["mmio_dma_ptr"], # dice has the ptr 
            size=other["buffer_size"],
            access_addrs = [] # dice does not have it 
        )
    diff = groundtruthdiffing.DifferentBufferType(detected_buf=obtained_buf, expected_buf=expected_buf)
    return diff

# analyze dice performance
def interpret_dice(dice_data, ground_truth):
    res = {}
    for name in ground_truth.keys():
        dice_entry = dice_data[name]
        gt_entry = ground_truth[name]
        # iterate all ground truth buffers for a single firmware
        for gt_buf, gt_mmio in gt_entry:
            # did dice find anything at all?
            if len(dice_entry) == 0:
                # if dice finds nothing, we need to add a missing buffer for each rx? or all?
                try:
                    tmp = res[name]
                except:
                    res[name] = []
                res[name].append(build_missingbuffer(gt_buf))
            for dice_config in dice_entry:
                # both are rx? We do not detect any problems
                if gt_buf["type"] == "r" and dice_config["type"] == "r" and gt_buf["buffer_address"] == dice_config["buffer_address"]:
                    try:
                        tmp = res[name]
                    except:
                        res[name] = []
                    accesses = []
                    res[name].append(build_correctclassification(gt_buf,dice_config))
                    break
                # both are tx? We do not detect any problems
                if gt_buf["type"] == "t" and dice_config["type"] == "t" and gt_buf["buffer_address"] == dice_config["buffer_address"]:
                    # in theory, there can be a problem: if dice never reaches the buffer because of fuzzer limitations, 
                    # it could happen that this fuzzer limitation shadows a misclassification
                    # we skip this case here
                    try:
                        tmp = res[name]
                    except:
                        res[name] = []
                    accesses = []
                    res[name].append(build_correctclassification(gt_buf,dice_config))
                    break
                # dice says rx, ground truth says tx? -> Dice accesses the buffer and misclassifies it 
                # detection issue, record as such
                if gt_buf["type"] == "t" and dice_config["type"] == "r" and gt_buf["buffer_address"] == dice_config["buffer_address"]:
                    try:
                        tmp = res[name]
                    except:
                        res[name] = []
                    accesses = []
                    res[name].append(build_differentbuffertype(gt_buf,dice_config))
                    break
                # dice says tx, groudn truth says rx?
                # two options:
                # first option: if the firmware never accesses the buffer, we have a strange firmware that never accesses its input, but the classifications are ok
                # second option: if the fuzzer never reaches the point in the firmware where the buffer is accesed, it might be misclassified. This is a fuzzer limitation
                if gt_buf["type"] == "r" and dice_config["type"] == "t" and gt_buf["buffer_address"] == dice_config["buffer_address"]:
                    try:
                        tmp = res[name]
                    except:
                        res[name] = []
                    res[name].append(build_differentbuffertype(gt_buf,dice_config))
                    break
                # at this point, we know that if there was a buffer address match, we caught it
                # so everything that is here is either a gt buffer that was not found by dice or a dice buffer
                # that was not in the gt

                # investigate case 1: ground truth single
                # check that it really is a ground truth single
                found = False
                for tmp in dice_entry:
                    if tmp["buffer_address"] == gt_buf["buffer_address"]:
                        # it was, in fact, not a ground truth single
                        # this is covered in another iteration then
                        found = True
                        break
                if found:
                    break
                else:
                    # it was a ground truth single. Add it to the missing set
                    # but only if it was an rx config
                    if gt_buf["type"] == "r":
                        try:
                            tmp = res[name]
                        except:
                            res[name] = []
                        res[name].append(build_missingbuffer(gt_buf))
                    break
               
                found = False
                # confirm case 2: dice single
                for tmp_gt_buf, tmp_gt_mmio in gt_entry:
                    if tmp_gt_buf["buffer_address"] == dice_config["buffer_address"]:
                        # it was, in fact, not a ground truth single
                        # should theoretically be impossible here
                        found = True
                        break
                
                if found:
                    break
                else:
                    # it was a dice single. Add it to the missing set
                    try:
                        tmp = res[name]
                    except:
                        res[name] = []
                    res[name].append(build_additionalbuffer(dice_config))
                    break
                print(f"{name} is uncategorized")
                assert 0, "This should not happen"
    return res 


# for now, we use the following schema
# 1: correct
# 2: size wrong (can only appear for fuzzware)
# 3: missing descriptor (we only award missing descriptor if rx is missing, a missing tx is ignored for now)
# 4: wrong buffer classification (gt tx, detected rx)
# 5: fuzzer limitation (gt rx, detected tx) 


# dice notes that it cannot emulate "2 out of 9 dma controller types"
# it never explicitly mentions which are unsupported
# one that is mentioned is nrf easydma
# second one is unclear: in our experiments, it finds buffer candidates
# for all samples except sam3x arduino, which should be supported
NUM_ERRORS = 5
def create_table(ground_truth, gpdma_results, dice_results, case_mapping):
    table = Texttable()
    table.set_cols_align(["l", "l", "c", "c"])
    table.set_cols_valign(["m", "m", "m", "m"])
    table.header(["Board", "Sample name", "DICE", "GDMA"])
    tmp_rows = []
    # "\\greencheck" if gpdma_results[firmware] == "c" else "\\redcross"
    for firmware in ground_truth.keys():
        gpdma_val = gpdma_results[firmware]
        dice_val = dice_results[firmware]
        gpdma = [] 
        dice = [] 

        # we know of some fuzzer limitations from manual inspections
        # assign fuzzer limitations for both
        if firmware in FUZZWARE_LIMITATIONS:
            gpdma.append(CASE_5)
        if firmware in P2IM_LIMITATIONS:
            dice.append(CASE_5)

        # potential values for gdma descriptor diffs:
        # CorrectDummy, DifferentSize, MissingDescriptor
        for gpdma_buf in gpdma_val:
            # correct
            if type(gpdma_buf) == groundtruthdiffing.CorrectDummy:
                gpdma.append(CASE_1)
            # fuzzware reports wrong size range
            elif type(gpdma_buf) == diffing.DifferentSize:
                gpdma.append(CASE_2)
            # descriptor was not found, probably due to a fuzzer limitation
            elif type(gpdma_buf) == diffing.MissingDescriptor:
                gpdma.append(CASE_3)
            else:
                assert 0, f"Found unimplemented gdma type {type(gpdma_buf)}"

        if len(gpdma) > 1:
            err_types = 0
            for i in range(2,NUM_ERRORS+1):
                if i in gpdma:
                    err_types += 1
        gpdma = max(gpdma)
            
        # potential values for dice descriptor diffs:
        # CorrectClassification, DifferentBufferType, AdditionalBuffer, MissingBuffer

        for dice_buf in dice_val:
            # correct
            if type(dice_buf) == groundtruthdiffing.CorrectClassification:
                dice.append(CASE_1)
            elif type(dice_buf) == groundtruthdiffing.DifferentBufferType:
                # if we detect rx, but ground truth says tx, we have a detection issue
                if dice_buf.detected_buf.type == groundtruthdiffing.GroundTruthBufferType.RX:
                    dice.append(CASE_4)
                # if we detect tx, but ground truth says rx, the most likely scenario is a fuzzer limitation
                # as dice probably never accessed the buffer
                else:
                    dice.append(CASE_5)
            # descriptor was not found, probably due to a fuzzer limitation
            # or, in case of dice, a descriptor limitation
            # we assign missing descriptor
            elif type(dice_buf) == groundtruthdiffing.MissingBuffer:
                dice.append(CASE_3)
            else:
                assert 0, f"Found unimplemented dice type {type(dice_buf)}"


        if len(dice) > 1:
            err_types = 0
            for i in range(2,NUM_ERRORS+1):
                if i in dice:
                    err_types += 1
        # we take the highest number and issue a warning if there is more than 1 error
        dice = max(dice)
        tmp = [firmware, dice, gpdma]
        tmp_rows.append(tmp)
    for r in tmp_rows:
        # we have a row of numbers, map it to the symbols
        symbol_row = []
        for i in range(0,len(r)):
            # do not map the name
            # instead split it and put it as the first and second entry
            if i == 0:
                board = r[i].split("_")[0]
                sample = "_".join(r[i].split("_")[1:])
                symbol_row.append(board)
                symbol_row.append(sample)
                continue
            # map everything else
            symbol_row.append(case_mapping[r[i]])
        table.add_row(symbol_row)
    return table


def main():
    parser = argparse.ArgumentParser(prog='table-creator')
    parser.add_argument('--latex', action="store_true", default=False, help="Output latex table instead of ascii")
    parser.add_argument('--dice-file', type=Path, required=True, default=None, help="Path to dice perspective")
    parser.add_argument('--groundtruth', type=Path, required=True, default=None, help="Path to ground truth")
    # first step: invoke cli.py diff to create the gpdma file
    # this needs 4 arguments: the run dir, the name, groundtruth type and the groundtruth root
    # run dir needs to be specified, groundtruth type is static "groundtruth-yaml", name is static ""
    parser.add_argument('--gpdma-run', type=Path, required=True, default=None, help="Path to a run of gpdma that we want to evaluate")
    args = parser.parse_args()
    
    # groundtruth root is the parent dir of groundtruth
    groundtruth_root = args.groundtruth.parent.absolute()

    # build fake args
    fake_args = argparse.Namespace(name="", groundtruth_type="groundtruth-yaml", root=[str(args.gpdma_run)], groundtruth_root=groundtruth_root, verbose=False, ref_name=None, num_cores=1, perf=False, file=None, searchdir=args.gpdma_run)
    # now invoke diff
    diffing.model_diff_main(fake_args)

    dice_data = None
    data = None
    gpdma_data = None
    try:
        with open(args.dice_file,"r") as dice:
            dice_data = yaml.load(dice, Loader=yaml.Loader)
    except Exception as e:
        import traceback
        sys.err.write(f"Yaml parser error while parsing dice data: {traceback.print_exc()}")
        exit()
    try:
        with open(args.groundtruth,"r") as d:
            data = yaml.load(d,Loader=yaml.Loader)
    except Exception as e:
        import traceback
        sys.err.write(f"Yaml parser error while parsing groundtruth data: {traceback.print_exc()}")
        exit()
    try:
        # the file is generated in the diff invocation above
        tmp_dir = Path("results-01.yml")
        with open(tmp_dir,"r") as d:
            gpdma_data = yaml.load(d,Loader=yaml.Loader)
        tmp_dir.unlink()
    except Exception as e:
        import traceback
        sys.stderr.write(f"Yaml parser error while parsing gpdma data: {traceback.print_exc()}")
        exit()
    assert dice_data, "Could not load dice data"
    assert gpdma_data, "Could not load gpdma data"
    assert data, "Could not load our input data"
    
    ground_truth = parse_ground_truth(data)
    dice_dict = parse_dice(dice_data)
    assert ground_truth.keys() == dice_dict.keys(), "Difference in samples between dice and ground truth"
    
    gpdma_results = parse_and_interpret_gpdma(gpdma_data, ground_truth)
    print(f"Num samples: {NUM_SAMPLES}, got {len(gpdma_results)}")
    assert len(gpdma_results.keys()) == NUM_SAMPLES, "Number of analyzed gpdma samples is incomplete!"

    # check now dice perspective
    dice_results = interpret_dice(dice_dict, ground_truth)
    assert len(dice_results.keys()) == NUM_SAMPLES, "Number of analyzed dice samples is incomplete!"
    if args.latex:
        # 1: correct
        # 2: min size wrong (can only appear for fuzzware). We mark as passed as we fill the buffer iteratively.
        # 3: missing descriptor (we only award missing descriptor if rx is missing, a missing tx is ignored as it is not relevant for fuzzing)
        # 4: wrong buffer classification (ground truth tx, detected rx)
        # 5: fuzzer limitation (ground truth rx, detected tx for dice, fuzzer did not reach dma access for dice and fuzzware) 
        case_mapping = {
                1: "\cmark",
                2: "\cmark",
                3: "\\xmark",
                4: "(\\xmark)",
                5: "(\cmark)",
                }
        table = create_table(ground_truth, gpdma_results, dice_results, case_mapping)
        print(latextable.draw_latex(table,alias={"_": "\\_"},use_booktabs=True))
    else:
        case_mapping = {
                1: "correct",
                2: "correct",
                3: "undetected descriptor",
                4: "wrong transfer direction",
                5: "fuzzer limitation",
                }
        table = create_table(ground_truth, gpdma_results, dice_results, case_mapping)
        print(table.draw())


if __name__ == "__main__":
    main()
