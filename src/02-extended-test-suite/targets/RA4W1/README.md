# ra4w1_serial_contiguous sample
The sample is based on the [example project bundle](https://www.renesas.com/us/en/document/scd/ek-ra4w1-example-project-bundle), and more specifically the `dma_spi` sample. The Main Menu and the SPI Slave have been removed. Instead, the Master reads from SPI and then calls `check_password` on the resulting buffer.

## Prerequisites
None

## Building our samples
Run `build_docker.sh`
Otherwise, download the renesas fsp and use the e2studio ide to build it.

## Creating a new Renesas RA sample
Take a sample out of the IDE samples. Modify it to your needs and build it in the IDE.
