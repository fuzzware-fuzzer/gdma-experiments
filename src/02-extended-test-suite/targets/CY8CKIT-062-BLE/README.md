# CY8CKIT-062

## Prerequisites
- Download `ModusToolbox_3.2.0.16028-linux-install.deb` (Version `3.2.0.16028`, Linux x64 deb) from https://softwaretools.infineon.com/tools/com.ifx.tb.tool.modustoolbox (requires account)

## Building
Run docker, or
- install modustoolbox
- get https://github.com/Infineon/mtb-example-psoc6-uart-transmit-receive-dma via the project creator cli in modustoolbox (we used `release-v3.1.0`)
- apply the patch file to the matching source file 
- patch the `CY_TOOLS_PATHS` variable in the Makefile to contain the path of your modustoolbox installation
- run the makefile: `make getlibs; make build`

## Creating a new sample
- install modustoolbox
- get a sample from infineon github and modify it to your needs. We used https://github.com/Infineon/mtb-example-psoc6-uart-transmit-receive-dma, tag `release-v3.1.0`
- patch the `CY_TOOLS_PATHS` variable in the Makefile to contain the path of your modustoolbox installation
- run the makefile: `make getlibs; make build`
