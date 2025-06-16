import yaml
import os


def load_ground_truth(path):
    res = {}
    with open(path,"r") as f:
        ground_truth = yaml.safe_load(f)
        for k in ground_truth.keys():
            instance = ground_truth[k]
            # for each sample, I want 
            # the name
            # the buffer address
            # the buffer size

            # name
            name = instance["name"]
            res[name] = []
            # there might be multiple buffers, collect all
            # key is "buf0","buf1",...
            i = 0
            while True:
                key = "buf" + str(i)
                try:
                    # not dead yet
                    # if we survive this, there is a buffer
                    buf = instance[key]
                    buf_addr = buf["buffer_address"]
                    buf_size = buf["buffer_size"]
                    buf_type = buf["type"]
                    # build a tuple that describes the buffer and add it to the result
                    res[name].append((name, buf_addr, buf_size, buf_type))
                    i = i + 1
                except KeyError:
                    # buffer does not exist anymore
                    break
    return res


def find_all_generated_configs(path):
    res = []
    for subdir, dirs, files in os.walk(path):
        for file in files:
            if "dma_config.yml" in files:
                res.append(os.path.abspath(os.path.join(subdir,"dma_config.yml")))
    return res


# equality check: check the buffer descriptors
# if the address is the same and the size less than or equal to discovered 
def equality_check(generated, ground_truth):
    gt_name, gt_addr, gt_size, gt_type = ground_truth
    data = generated["peripherals"]["my_dma_periph"]
    # the known_sizes field contains both the address and the sizes
    # check if the address is there
    try:
        # this only works if the address we found is in the ground truth
        sizes = data["known_sizes"][gt_addr]
        small = sizes["min"]
        big = sizes["max"]
        # size does not matter, unless min size > gt size
        if small > gt_size: 
            return False
        return True
    except KeyError as e:
        return None 


def perform_analysis(generated_configs, ground_truth, out_path):
    res = {}
    # we want to check "equality" for each generated config, for some definition of equality
    for config in generated_configs:
        with open(config,"r") as f:
            config_loaded = yaml.safe_load(f)
            # we will identify the matching ground truth
            # by splitting at the separator and checking if there is a
            # fragment of the path that equals the ground truth name
            # WARNING this breaks if we have / in the pathnames
            fragments = config.split(os.path.sep)
            found = None 
            for key in ground_truth.keys():
                buffers = ground_truth[key]
                # we can upgrade from None to False/True, and from False to True
                for entry in buffers:
                    name, _, _, _ = entry
                    if name in fragments:
                        tmp = equality_check(config_loaded, entry)
                        # nothing discovered yet, new result is None, False, True
                        if found is None and tmp is not None:
                            found = tmp
                        # only misconfigured buffer for now, but the new one is correct, so upgrade
                        if found==False and tmp==True:
                            found = tmp
                if found is None:
                    res[config] = "buffer not found"
                if found == True:
                    res[config] = "buffer equal"
                if found == False:
                    res[config] = "buffer size mismatch"
    with open(out_path, "w") as f:
        yaml.dump(res, f)
