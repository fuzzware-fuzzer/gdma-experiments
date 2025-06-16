# ra4w1_serial_contiguous_dtc sample
The sample is based on the [example project bundle](https://www.renesas.com/us/en/document/scd/ek-ra4w1-example-project-bundle), and more specifically the `spi` sample. 
The Main Menu and the SPI Slave have been removed. Instead, the Master reads from SPI and then calls `check_password` on the resulting buffer. 
In difference to the non `dtc` sample, this sample uses the Data Transfer Controller instead of the DMAC. 
As a result, configuration is (such as SRC and DST addresses) are not stored in MMIO registers. 
Instead, the configuration is kept in SRAM with a MMIO register pointing to it.

## Prerequisites
None

## Building our samples
Run `build_docker.sh`
Alternatively, get the renesas fsp and e2studio ide and build it via the ide.

## Creating a new Renesas RA sample
Installation of an IDE is possible, but not needed. The Dockerfile ships with a preinstalled IDE thats configured to perform headless compilation.
Just copy the `build_docker.sh` and adjust the `ra4w1_serial_contigious_dtc` path to your new project dir.
Otherwise, download the renesas fsp and use the e2studio ide to build it.
