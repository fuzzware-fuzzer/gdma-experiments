#!/bin/bash

# This script is to be run within the mbed-os docker container
BUILD_DIR=/opt/build
SOURCE_DIR=/opt/mbed-os
SAMPLE=BLE_GAP
SAMPLE_NAME=mbed-bluetooth

cd "$SOURCE_DIR"
# Restore git state for BLE example
git reset --hard
git clean -df
git checkout 711c5ca0ae6ba0253730db9d481b8f1462fd24e9
git submodule update --init
# apply fix for the build system
git apply /opt/samples/patches/fix_build.patch

# Restore git state for mbed-os submodule
cd mbed-os
git reset --hard
git clean -df
# checkout version with bugfixes
git checkout ed371ed04537cd0f01c32af6a069847310bc6cbe

# apply patches
git apply /opt/samples/patches/disable_float.patch
git apply /opt/samples/patches/bluetooth_dma_spi.patch

mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"
cmake "$SOURCE_DIR" -GNinja -DCMAKE_BUILD_TYPE=Develop -DMBED_TARGET=K64F
ninja "$SAMPLE"

# Copy sample to outside-visible directory
OUT_DIR="/workdir/output/$SAMPLE_NAME"
rm -rf /opt/samples/output 
mkdir -p /opt/samples/output
cp "${BUILD_DIR}/${SAMPLE}/${SAMPLE}.elf" /opt/samples/output 
