## renesas picohttpparser sample

The sample is based on the [example project bundle](https://www.renesas.com/us/en/document/scd/ek-ra4w1-example-project-bundle), and more specifically the `spi` sample. The Main Menu and the SPI Slave have been removed. Instead, the Master reads from SPI and then uses [picohttpparser](https://github.com/h2o/picohttpparser/) to try and parse the input as HTTP.

The sample is built for the Renesas RA4W1 board, and requires hardware floating point acceleration to be enabled.