#!/bin/bash
DIR="$(dirname "$(readlink -f "$0")")"

set -ex

# This script is to be run within the mbed-os docker container
BUILD_DIR=/tmp/build
SOURCE_DIR=/workdir/mbed-os
SAMPLE=BLE_GAP

cd "$SOURCE_DIR"
# Restore git state for BLE example
git reset --hard
git clean -df
git checkout 711c5ca0ae6ba0253730db9d481b8f1462fd24e9
git submodule update --init --force
# apply fix for the build system
git apply $DIR/patches/fix_build.patch

# Restore git state for mbed-os submodule
cd mbed-os
git reset --hard
git clean -df
# checkout version with bugfixes
git checkout 44dabfb15d17526ec5cab31965cc3d593c8e98b2

# revert specific bugfix commit
git revert --no-commit "$REVERT_COMMIT"

# apply patches
git apply $DIR/patches/disable_float.patch
git apply $DIR/patches/bluetooth_dma_spi.patch

mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"
cmake "$SOURCE_DIR" -GNinja -DCMAKE_BUILD_TYPE=Develop -DMBED_TARGET=K64F
ninja "$SAMPLE"

# Copy sample to outside-visible directory
OUT_DIR="/workdir/rebuilt/$CVE_NUM"
rm -rf $OUT_DIR
mkdir -p $OUT_DIR
cp "${BUILD_DIR}/${SAMPLE}/${SAMPLE}.elf" $OUT_DIR
