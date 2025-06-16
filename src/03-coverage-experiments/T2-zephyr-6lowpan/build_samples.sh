#!/bin/bash
# This script is to be run within the zephyr CI docker container

set -x
set -e

# export SAMPLE=6lowpan
# export SAMPLE_NAME=zephyr-6lowpan
# export BASE_COMMIT=v3.5.0
# 
# export BOARD=nrf52840dongle_nrf52840
# export ZEPHYR_VERSION=3.5.0
# export OVERLAYS=overlay-802154.conf
# 
# export SAMPLE_DIR=samples/net/sockets/echo_server
# export EXTRA_DEFINES="-DCONFIG_SHELL=n -DCONFIG_NET_SHELL=n -DCONFIG_NET_L2_IEEE802154_SHELL=n -DCONFIG_NET_SHELL_DYN_CMD_COMPLETION=n "

# Create zephyr workspace for the given version if needed
# workspace_dir=/workdir/workspace-$ZEPHYR_VERSION
cd /opt/zephyr/zephyr
export ZEPHYR_BASE=$(pwd)
git apply /opt/samples/patches/ieee802154_reass_timeout.patch
git apply /opt/samples/patches/wdt_sam_watchdog_callback_check.patch

# Build sample
cd samples/net/sockets/echo_server
rm -rf build
west build --pristine always -b nrf52840dongle_nrf52840 . -- -DOVERLAY_CONFIG=overlay-802154.conf -DCONFIG_SHELL=n -DCONFIG_NET_SHELL=n -DCONFIG_NET_L2_IEEE802154_SHELL=n -DCONFIG_NET_SHELL_DYN_CMD_COMPLETION=n

# Copy sample to outside-visible directory
cp build/zephyr/zephyr.elf "/opt/samples/output"
