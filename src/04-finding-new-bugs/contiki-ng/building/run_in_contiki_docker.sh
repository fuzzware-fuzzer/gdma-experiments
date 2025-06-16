#!/bin/bash
DIR="$(dirname "$(readlink -f "$0")")"

# This build env is known to allow builds of contiki-ng version 4.4 samples
CONTIKI_DOCKER_VERSION=c9a0e2c8af3f6fa0feb88bb642c471fb72c2ba952f4eae404d993712d603ee44

base_dir="$(realpath $DIR/..)"

# See if we have already cloned contiki-ng sources
if [ ! -e "$base_dir/contiki-ng" ]; then
    git clone https://github.com/contiki-ng/contiki-ng "$base_dir/contiki-ng"
    git -C "$base_dir/contiki-ng" checkout release/v4.9
fi

# Map our base dir and run the actual command (which will be one of the build scripts normally)
docker run --rm -ti --env "LOCAL_UID=$(id -u)" --env "LOCAL_GID=$(id -g)" -v $base_dir:/workdir --workdir=/workdir contiker/contiki-ng:$CONTIKI_DOCKER_VERSION $@
