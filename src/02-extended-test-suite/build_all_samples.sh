#/bin/bash
# script to iterate through all target directories and call the respective build script
# the rebuilt targets will be in $build_name/output/$sample_name/$sample.elf
set -x
DIR="$(dirname "$(readlink -f "$0")")"

# build the base image
cd "$DIR/common/"
docker build . -t password-base
cd $DIR

# I can probably shorten this to one line with find, like "find . -name build_docker.sh -execdir sudo sh {} \;"
find $DIR/targets -name build_docker.sh -execdir sh build_docker.sh \;

# # build the radio sample
# cd radio/NRF52832; sh build_docker.sh; cd $base_dir
# 
# # build nrf contiguous serial sample
# cd serial-contiguous/NRF52832; sh build_docker.sh; cd $base_dir
# 
# # build atmel contiguous serial sample
# cd serial-contiguous/SAM3X; sh build_docker.sh; cd $base_dir
# 
# # build nuvoton serial sample
# cd serial-contiguous/NUC123; sh build_docker.sh; cd $base_dir
# 
# # build contiguous mk64f sample (slow!)
# cd serial-contiguous/MK64F; sh build_docker.sh; cd $base_dir
# 
# # build atmel sg serial sample
# cd serial-scatter-gather/SAM3X; sh build_docker.sh; cd $base_dir
# 
# # build mk64f sg serial sample
# cd serial-scatter-gather/MK64F; sh build_docker.sh; cd $base_dir
# 
# # build mk64f ethernet sample 
# cd ethernet/MK64F; sh build_docker.sh; cd $base_dir
