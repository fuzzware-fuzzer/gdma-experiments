# Setting up the docker
These are the steps to set up the docker used for the eval. This was originally done with Ubuntu 22.04
As P2IM and DICE use a docker build system for qemu, we build DICE and P2IM on the host system and copy it into the docker.
If you do not use Ubuntu 22.04 it is possible that the reulting DICE and P2IM versions do not work with the Ubuntu used in the Dockerfile.  

In that case you may either run the experiments locally, which requires some adaption of the scripts, or you change the Dockerfile to use the OS you built DICE and P2IM with.

However, what should always work is using docker load to load the prebuilt docker with the tag `dice_tag`.

The steps to replicate this docker are:

## 1. DICE
Run the `create_dice.sh` script.  
This script downloads DICE, builds qemu and patches some of the python files to allow for configurable timeouts.  
Patches are located in the patch directory.

## 2. P2IM
Run the `create_p2im.sh` script
This script downloads DICE and removes all DMA related code from the qemu sources, that were added by DICE.
It then builds qemu and patches some of the python files to allow for configurable timeouts.  
Patches are located in the patch directory.  

The reason why we clone DICE and patch it instead of getting P2IM is because P2IM does not support all of the targets in the DICE dataset.  
As the code that is added by DICE to support the new boards is intertwined with some code used by the DMA functionality, it is more feasible to just remove the DMA functionality instead of porting  code to P2IM.

## 3. Configs
All configurations are derived from the orginal DICE target configurations. However, we  modified the paths to point to the dice/p2im qemu binary and the respective fuzzing bases. All configs are located in `p2im_configs`/`dice_configs`

## 4. Building and running
To build (and run the docker) execute the `build_docker.sh` script.
Afterwards you can cd to `../01-evaluation` and run the actual evaluation.

