# Coverage Sample Zephyr-OS 6LoWPAN
The sample uses the zephyr-os `echo_server` example application on the board `nrf52840dongle_nrf52840`.
This automatically includes the 6LoWPAN stack from zephyr-os.

## Building the Sample
The build requires docker to be installed and running.
Then execute `./rebuild_targets.sh`.
This will download all necessary components and build the firmware sample.

## Patches
The firmware is mostly unmodified from version 3.5.0 of zephyr-os.
The modifications are:
1. Prevent a crash due to usage of an uninitialized callback function
2. Prevent a crash due to usage of a timer that already went out of scope
