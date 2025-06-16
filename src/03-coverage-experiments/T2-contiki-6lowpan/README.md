# Coverage Sample Contiki-NG 6LoWPAN
The sample uses the contiki-ng `hello-world` example application on the board `nrf52840/dongle`.
This automatically includes the 6LoWPAN stack from contiki-ng.

## Building the Sample
The build requires docker to be installed and running.
Then execute `./rebuild_targets.sh`.
This will download all necessary components and build the firmware sample.

## Patches
The firmware is mostly unmodified from v4.9 of contiki-ng.
The modifications are:
1. Fix CVE-2023-48229 to avoid crashes in the coverage experiments
2. Disable hard float usage, as it is not supported by fuzzware
2. Enable debug information for debugging
