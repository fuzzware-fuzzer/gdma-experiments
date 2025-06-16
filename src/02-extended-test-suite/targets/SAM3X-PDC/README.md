# Atmel/Microchip Password sample

## Prerequisites
None for the docker build, for new samples, a windows installation is needed.

## Building
Build via docker, or
- On Windows, this is as simple as importing the project file and building via Atmel Studio
- On Linux, the makefile in `<solution>/Debug` should work

## Creating a new atmel/microchip sample
- Download and install Atmel Studio (Windows-only, we used [this](https://ww1.microchip.com/downloads/aemDocuments/documents/DEV/ProductDocuments/SoftwareTools/as-installer-7.0.2594-full.exe) version)
- Open a sample project: File > New > Example Project, then select board and example, alternatively create a new blank one
- This project is based on the `USART DMAC Example - SAM3X-EK` sample, patching the `usart_example_dmac.c` file with the matching patch file
- Build the project: Build > Build Solution
- This creates a makefile in the solution folder (`<solution>/Debug`), which basically runs out of the box on Windows. On Linux, you need to change the binutils paths to the respective paths on your system. In our samples, we provide a `replace.sh` file to automate this step. It assumes the required binutils (`arm-none-eabi-*`) to be in path. Also, you need add a symlink in the `Debug` folder to `../src`.
- Now, you can run the makefile and build the firmware
