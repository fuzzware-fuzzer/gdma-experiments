# CVE Samples Mbed-OS Bluetooth
The sample uses the mbed-os `BLE_GAP` example application from [mbed-os-examples-ble](https://github.com/mbed-ce/mbed-os-example-ble/tree/development/BLE_GAP) on the board `K64F`.
This automatically includes the Cordio Bluetooth stack that is used by mbed-os.

## Building the Sample
The build requires docker to be installed and running.
Then execute `./rebuild_targets.sh`.
This will download all necessary components and build the firmware sample.

## Patches
The firmware is slightly modified version of mbed-os from commit `ed371ed04537cd0f01c32af6a069847310bc6cbe`.
The modifications are:
1. Use DMA instead of MMIO to receive the Bluetooth HCI packets
2. Disable hard float usage, as it is not supported by fuzzware
