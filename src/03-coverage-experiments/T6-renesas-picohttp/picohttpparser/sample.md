## renesas picohttpparser sample

The sample is based on the [example project bundle](https://www.renesas.com/us/en/document/scd/ek-ra4w1-example-project-bundle), and more specifically the `spi` sample. The Main Menu and the SPI Slave have been removed. Instead, the Master reads from SPI and then uses [picohttpparser](https://github.com/h2o/picohttpparser/) to try and parse the input as HTTP.

See the sample.diff in this folder for a list of changes.

## Creating a new Renesas RA sample

Installation of an IDE is possible, but not needed. The Dockerfile ships with a preinstalled IDE thats configured to perform headless compilation.
Just copy the `../build_sample_picohttpparser.sh` and adjust the pathes inside to your new project dir.

## Building our samples

Run `../build_sample_picohttpparser.sh`
