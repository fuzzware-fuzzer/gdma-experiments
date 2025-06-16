## renesas HCI parser sample

The sample is based on the [example project bundle](https://www.renesas.com/us/en/document/scd/ek-ra4w1-example-project-bundle), and more specifically the `spi` sample. The Main Menu and the SPI Slave have been removed. Instead, the Master reads from SPI and then uses  the HCI parser from [bluez](https://github.com/bluez/bluez/) to try and parse the input as HCI packets.

See the [patches](/patches) directory in this folder for a list of changes.

## Creating a new Renesas RA sample

Installation of an IDE is possible, but not needed. The Dockerfile ships with a preinstalled IDE that's configured to perform headless compilation.
Just copy the `../build_sample_hciparser.sh` and adjust the paths inside to your new project dir.

## Building our samples

Run `../build_sample_hciparser.sh`
