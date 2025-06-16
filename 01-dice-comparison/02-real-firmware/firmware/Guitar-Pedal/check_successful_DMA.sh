#!/bin/sh

fuzzware_project="$1"

# An interesting case (but not expressible via a single milestone BB is):
# fuzzware cov 0x80013dc --exclude 0x080013ba
# This case represents the (adc_sample>=0.501) case
# The extra filter is required as the basic block 0x80013dc is re-used for control flow
if fuzzware cov 0x80013dc --exclude 0x080013ba -p $fuzzware_project | grep -v -A 1 "Could not find"; then
    echo "Success! Found coverage that indicates non-null DMA buffer contents"
    exit 0
else
    echo "Not yet found ..."
    exit 1
fi
