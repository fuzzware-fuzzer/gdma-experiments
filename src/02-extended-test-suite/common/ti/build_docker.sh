#!/bin/sh
DIR="$(dirname "$(readlink -f "$0")")"

$DIR/create_container.sh

mkdir -p output

$DIR/run_docker.sh ./build_samples.sh output
