# LPC1837 RAM-based SS7 parser sample
- UART sample that tests different UART modes based on the user's input
- We modified the firmware to only test DMA transfers
- ***We added Scatter gather descriptors instead of flat mmio-based buffers***

# Requirements
- Download mcuxpresso from [here](https://www.nxp.com/design/design-center/software/development-software/mcuxpresso-software-and-tools-/mcuxpresso-integrated-development-environment-ide:MCUXpresso-IDE) and place it in this directory
- For exact replication use version 11.10.0_3148, otherwise some paths in the Dockerfile may need to be adapted. The least requirement is to change the version string in the Dockerfile

# Building
TL;DR Just execute the build docker script, and check the output directory.
More details:
- The sample is based on the periph_uart sample, included in the SDK.
- The SS7 library can be downloaded from [here](https://github.com/asterisk/libss7/archive/03e81bcd0d28ff25d4c77c78351ddadc82ff5c3f.zip)
- Patches added to the main logic are detailed in the patch file
