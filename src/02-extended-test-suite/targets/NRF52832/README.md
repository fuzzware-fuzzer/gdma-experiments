# NRF52 Password sample
- UART sample from the NRF52 SDK
- Receive UART data byte by byte
- Modified to perform the password check on the data and reset the buffer after 8 receptions

## Prerequisites
None

## Building
TL;DR: Just run the build\_docker script.  
More details:
- The sample is based on the example/peripherals/uart sample in the SDK
- Patches to the main logic are documented in the [patch file](./main.patch)
- Furthermore, the [pw\_check.h](./uart_example/pw_check.h) is added to the source folder
- For ease of compilation, the board specific folder is replaced by a [minimal version](./uart_example/pca10040)

## Creating a new nrf52 sample
- Download and extract the sdk from [here](https://www.nordicsemi.com/Products/Development-software/nrf5-sdk/download)
- take an example inside the sdk and make a copy right next to it (they use relative paths to include additional makefiles, thus changing the relative path is quite a mess to fix). Good starting points are in `examples/peripheral`, e.g. the radio sample is a modified copy of `examples/peripheral/radio/receiver`.
- change the compiler path in `components/toolchain/gcc/Makefile.posix`
- navigate to the makefile: `<your_example>/pca<part_number>/blank/armgcc` and run it
- if you want to add it to the docker, you need to download the sdk inside docker and follow the same steps

