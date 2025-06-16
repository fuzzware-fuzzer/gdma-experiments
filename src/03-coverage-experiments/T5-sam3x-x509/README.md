# Coverage sample - x509 mbedTLS Certificate Parser
This sample is based on the ram-based SAM3x sample. The UART data, transferred by the DMA controller is inserted into x509 certificate parser function from the mbedTLS library.  
IF no DMA is available, the parser is executed with a zeroed buffer.

# Building the sample
TL;DR: Just run the docker build script
## Cross compiling mbedTLS
We already cross-compiled mbedTLS and provide the compiled libraries, however to compile it yourself, follow these steps:
- Clone https://github.com/Mbed-TLS/mbedtls/tree/development (commit f4f37eced7c39db5db4c6b5c5c6ec98bd81fe416)
- (git) apply the [mbedtls.patch](.mbedtls.patch) file. This file configures mbedTLS to run on an embedded system
- From the root folder compile via `make clean;  make CC=arm-none-eabi-gcc CFLAGS=-mcpu=cortex-m3 lib`
	- You need the cross-compiler arm-none-eabi-gcc
	- -mcpu=cortex-m3 tells the compiler to which architecture (and ISA) to compile to
	- lib only compiles the libraries
- The libraries are located in library/
- copy all libraries to `sam3x_uart_scatter_gather/USART_USART_DMAC_EXAMPLE1/src/ASF/thirdparty/CMSIS/Lib/GCC/`

## Compiling the USART sample
Apart from the cross compiled libraries (and the subsequent changes in the Makefile) we added small changes to the [source file](sam3x_uart_scatter/USART_USART_DMAC_EXAMPLE1/src/usart_example_dmac.c). Namely:
- We added a third DMA buffer and the according control struct
- We made the buffers larger
- We initialize the x509 parser in the main function
- In the `DMAC_Handler` we copy all DMA buffer contents to a singular buffer and let the x509 library parse this data as a certificate.

These change are also part of the according [patch file](./usart_example_dmac.patch). However these patches are only in relation to the ram-based password sample and not to the original atmel source code

Note: The docker file still clones mbedtls, however this is only necessary for the headers, as the pre-compiled libraries are already supplied with the sample
