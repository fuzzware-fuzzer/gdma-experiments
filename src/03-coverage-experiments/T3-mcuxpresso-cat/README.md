# Coverage Samples Based on Mcuxpresso
The samples uses the [mcux-sdk](https://github.com/nxp-mcuxpresso/mcux-sdk) from NXP.

## Building the Sample
The build requires docker to be installed and running.
Then execute `./rebuild_targets.sh`.
This will download all necessary components and build the firmware samples.

## cAT
This sample uses the [cAT](https://github.com/marcinbor85/cAT) AT command parser on the board `frdmk64f`.

### Source Code
The firmware is build on the `edma_transfer` example application from the mcux-sdk and passes the UART input to the cAT parser.
To setup the cAT parser the included demo application is used.
The code of the `edma_transfer` example and the cAT demo have been modified to save the UART input into a buffer and then process it with the parser.
For more details look at the files [`uart_edma_transfer.patch`](cat/patches/uart_edma_transfer.patch) and [`demo.patch`](cat/patches/demo.patch).
