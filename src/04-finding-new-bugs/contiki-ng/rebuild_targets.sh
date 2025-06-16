#!/bin/bash
DIR="$(dirname "$(readlink -f "$0")")"

set -e

# Compile targets in docker environment
for build_file in "$DIR/building"/build_sample_*.sh; do
    $DIR/building/run_in_contiki_docker.sh /workdir/building/$(basename $build_file)
done

NEWLY_BUILT_DIR=$DIR/rebuilt
echo "rebuilt targets are located at $NEWLY_BUILT_DIR"
