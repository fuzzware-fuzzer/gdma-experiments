# Building the EFM32 Coverage sample
## Sample
This sample is a merge of the ram-based password sample already used in 02-extended-test-suite and an [MQTT parser](https://github.com/deoxxa/mqtt-protocol-c/tree/master).  
The source files of the MQTT parser are co-located in the same directory as the main logic.  

## Patches
There are some small patches compared to the password sample to include the MQTT parser. Those are visible in the according patch files.  

## Building
Running the docker script will yield the elf file in the output directory.  

For patching change the source files in the [project directory](./projects). 
Unless new files need to be included this should be easily possible



# General
## Creating a new silabs sample
- This shows how we built our sample from a reference sample, the same idea applies for new samples
- install cli: https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-tools-slc-cli/02-installation  
- clone https://github.com/SiliconLabs/gecko_sdk.git  
- `./slc_cli/slc configuration --sdk=gecko_sdk/gecko_sdk.slcs`  
- `./slc_cli/slc signature trust --sdk gecko_sdk/gecko_sdk.slcs`  
- `./slc_cli/slc configuration --gcc-toolchain=/opt/gcc-arm-none-eabi-10-2020-q4-major`  
- `./slc_cli/slc generate gecko_sdk/app/common/example/uartdrv_baremetal/uartdrv_baremetal.slcp -np -d=projects/ -name=test --with brd2001a`  
- fix `config/sl_uartdrv_leuart...` (`make -f test.Makefile` tells you the problems. In our case, you can apply the matching patch file)  
- patch `uartdrv_app.c` with the matching patch file to recreate our sample
- remove the broken linker flag (something rwx `--no-warn-rwx-segments` in test.project.mak) 
- this is the uart sample, the concept works with all the samples from the sdk

## Building with Docker
- no real problems, except for hardcoded paths, so make sure to recreate directory layout in docker
