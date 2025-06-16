#!/bin/bash
DIR="$(dirname "$(readlink -f "$0")")"

base_dir="$(realpath $DIR/..)"

# See if we have already cloned mbed-os sources
if [ ! -e "$base_dir/mbed-os" ]; then
    git clone https://github.com/mbed-ce/mbed-os-example-ble "$base_dir/mbed-os"
    git -C "$base_dir/mbed-os" checkout 711c5ca0ae6ba0253730db9d481b8f1462fd24e9
    git -C "$base_dir/mbed-os" submodule update --init --no-recommend-shallow # pull all commits
fi

docker build -t mbed-os "$DIR"
# Map our base dir and run the actual command (which will be one of the build scripts normally)
docker run --rm -ti --user="$(id -u)" -v "${base_dir}:/workdir" --tmpfs "/.ccache" --workdir=/workdir mbed-os $@
