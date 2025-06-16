# Silabs password sample
## Prerequisites
None for docker build, otherwise gecko sdk, slc cli

## Building
Use docker, or
- install cli: https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-tools-slc-cli/02-installation  
- clone https://github.com/SiliconLabs/gecko_sdk.git  
- `./slc_cli/slc configuration --sdk=gecko_sdk/gecko_sdk.slcs`  
- `./slc_cli/slc signature trust --sdk gecko_sdk/gecko_sdk.slcs`  
- `./slc_cli/slc configuration --gcc-toolchain=/opt/gcc-arm-none-eabi-10-2020-q4-major`  
- `./slc_cli/slc generate gecko_sdk/app/common/example/uartdrv_baremetal/uartdrv_baremetal.slcp -np -d=projects/ -name=test --with brd2001a`  
- fix `config/sl_uartdrv_leuart...` (`make -f test.Makefile` tells you the problems. In our case, you can apply the matching patch file)  
- patch `uartdrv_app.c` with the matching patch file to recreate our sample
- remove the broken linker flag (`--no-warn-rwx-segments` in test.project.mak) 

## Creating a new silabs sample
- install cli: https://docs.silabs.com/simplicity-studio-5-users-guide/latest/ss-5-users-guide-tools-slc-cli/02-installation  
- clone https://github.com/SiliconLabs/gecko_sdk.git  
- `./slc_cli/slc configuration --sdk=gecko_sdk/gecko_sdk.slcs`  
- `./slc_cli/slc signature trust --sdk gecko_sdk/gecko_sdk.slcs`  
- `./slc_cli/slc configuration --gcc-toolchain=/opt/gcc-arm-none-eabi-10-2020-q4-major`  
- pick any sample, and build it similar to the uartdrv sample above
- fix the Makefile (`make -f test.Makefile` tells you the problems)  
- remove the broken linker flag (`--no-warn-rwx-segments` in test.project.mak) 
