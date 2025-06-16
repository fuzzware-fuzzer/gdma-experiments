# MK64F Password sample
## Prerequisites
None

## Building
Use the docker build script, or:
- Download the sdk from [here](https://github.com/nxp-mcuxpresso/mcux-sdk) and follow the instructions to set it up (with west)
- Go to `examples/frdmk64f` (this contains the samples for this board)
- Modify an example to your needs (we used `driver_examples/uart/edma_transfer`)
- Apply the patch file to recreate our sample
- Inside the example folder, go into the `armgcc` folder
- Export your compiler dir (locally, I set `export ARMGCC_DIR=/usr/`, check docker file how to set it up with a different location)
- Run `build_all.sh`
- Your binaries are in `release` or `debug`

## Creating a new sample
Start from one of the examples in the `examples/` folder, modify it to your needs, and then follow the same steps as above.
