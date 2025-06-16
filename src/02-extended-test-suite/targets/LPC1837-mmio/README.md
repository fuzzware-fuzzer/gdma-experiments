# LPC1837 password sample 
- UART sample that tests different UART modes based on the user's input
- In DMA mode we modified the firmware to receive data and perform the password check
- Afterward, the next UART mode isagfain based on the user's input.

## Prerequisite
- Download mcuxpresso from [here](https://www.nxp.com/design/design-center/software/development-software/mcuxpresso-software-and-tools-/mcuxpresso-integrated-development-environment-ide:MCUXpresso-IDE) and place it in this directory
- For exact replication use version 11.10.0_3148, otherwise some paths in the Dockerfile may need to be adapted. The least requirement is to change the version string in the Dockerfile

## Building
TL;DR Just execute the build docker script, and check the output directory.
More detail:
- The sample is based on the periph\_uart sample, included in the SDK.
- Patches added to the main logic are detailed in the [patch file](./main.patch)
- Furthermore, the [pw\_check.h](./periph_uart/pw_check.h) is added to the source folder
 
## Creating a new sample
If you base your work on a sample from the ide, you can copy over the changed files, similar to what is done for the uart example.
