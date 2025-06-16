#!/bin/bash


set -x
if [ -d p2im_dice ] ; then
	rm -rf p2im_dice
fi
mkdir -p p2im_dice
cd p2im_dice

# Download and initialize the repo
git clone https://github.com/RiS3-Lab/DICE-DMA-Emulation.git
cd DICE-DMA-Emulation
git rm mips-emulator
git submodule update --init --recursive

# Build qemu for the first time
cd p2im/qemu
git clone https://github.com/xgandiaga/DRIVERS.git
WORK_FOLDER_PATH=`pwd`/src ./DRIVERS/build-qemu.sh --deb64 --no-strip
cd -

# Apply p2im specific patches
pwd
cp ../../patches/p2im_specific.patch ./DICE-Patches/DICE-P2IM.patch
git apply ./DICE-Patches/DICE-P2IM.patch --unsafe-paths --directory ./p2im/qemu/src/qemu.git/


# Build qemu for the second time
cd p2im/qemu
WORK_FOLDER_PATH=`pwd`/src ./DRIVERS/build-qemu.sh --deb64 --no-strip

# PAtch the binary to avoid GLIBC error
cd src/install/debian64/qemu/bin/
patchelf --replace-needed librt.so.1 /lib/x86_64-linux-gnu/librt.so.1 qemu-system-gnuarmeclipse
cd ../../../../../../../

# Build AFL
cd p2im
make -C afl/
cd -

# Apply our patches
cp ../../patches/*.patch .
# Add fuzzing timeout of 24h
git apply fuzzing.patch
