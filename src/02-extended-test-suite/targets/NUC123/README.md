# Nuvoton NUC123 password sample

## Prerequisites
None

## Building 
- This requires that you built it at least once with the GUI as it creates the required makefiles
- Navigate to the folder that contains the source of your example
- Go into `GCC/{Debug/Release}/`, it contains a `makefile`
- Checkout the entry for the final `.elf` file and note down the hardcoded path
- In your docker environment, you need to recreate this path: you need to put both the `Library` folder and the `SampleCode` folder to the correct hardcoded path
- E.g. `/home/ubuntu/NUC123BSP/{SampleCode/Library}` in our example
- once you did this, you can run the makefiles and it will create your binaries

## Creating a new nuvoton sample 
- Download the IDE [NuEclipse](https://www.nuvoton.com/tool-and-software/ide-and-compiler/) and install it
- Download the board support package from github, e.g. the one for the NUC123 is [here](https://github.com/OpenNuvoton/NUC123BSP)
- This sample is based on the `StdDriver/UART_PDMA` sample with `main.c` modified according to the patch file (commit `d5d7eaaa06fa87e0e713c0b75c6b92a6c47c5323`)
- Open an example from the BSP that is close to your requirements and edit it according to your needs
- Build it via the GUI
- Now follow the steps in building
