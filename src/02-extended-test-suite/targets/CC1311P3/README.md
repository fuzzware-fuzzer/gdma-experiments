# TI Samples

## Prerequisites
None for the docker build, otherwise you need the sdk and code composer studio.

## Building

> WARNING: The used IDE produces abosolute paths as part of its build process. As a result, the setup depends heavily on exactly matching paths. As such, if you would like to reproduce the projects, take extra care in following the build instructions. Using different usernames within the VM or workspace locations may result in failing builds, troubleshooting and the requirement of adjusting the docker container.

These samples are built using the [SimpleLink SDK](https://www.ti.com/tool/download/SIMPLELINK-LOWPOWER-F2-SDK/7.41.00.17).

The Dockerfile will install the version of GCC that is used by TI Code Composer Studio (CCS) version 12.

The project files with the sample source code have been generated using the Code Composer Studio GUI on a Ubuntu Desktop 22.04.

For the provided projects, you can re-build the firmware by running:

```shell
./build_docker.sh
```


## Creating a new sample

### Installing Code Composer Studio in VM
1. Set up an Ubuntu 22.04 Desktop VM
    - Choose username: `user` (for the best compatibility with the provided docker build env)
    - If the username `user` is not chosen, the docker container will have to be adjusted later
2. Install required dependencies inside the vm
```
sudo apt-get install gcc-multilib libpython2.7-dev libtinfo5 libgconf-2-4 libusb-dev
```
3. Download and run the installer of TI Code Composer Studio (CCS):
```
# Download CCS
wget -O ~/Downloads/CCS.tar.gz --progress=dot:giga https://dr-download.ti.com/software-development/ide-configuration-compiler-or-debugger/MD-J1VdearkvK/12.7.1/CCS12.7.1.00001_linux-x64.tar.gz && tar -xf ~/Downloads/CCS.tar.gz --directory ~/Downloads
# Run CCS installer
~/Downloads/CCS*/ccs_setup_*.run
```
4. During installation
- ensure that all dependency checks pass. Otherwise, install the missing dependencies and go back->forward to re-check the requirements
- For the installation location, choose `~/ti/ccs` (without the default version number)
- *Setup Type*: Choose "Custom Installation" -> Forward
- *Select Components*: Check "Wireless connectivity" -> Forward
- Press "Forward" through the rest of the install process

### Reproducing the Source Code Project

To create a new target to build, take the following steps in the CCS GUI:

1. Run CCS with `~/ti/workspace` as workspace location
```sh
~/ti/ccs/ccs/eclipse/ccstudio -data ~/ti/workspace
```
2. On first CCS run, within the CCS GUI install GCC
    - In Code Composer Studio GUI, Help->Install GCC ARM Compiler Tools...
    - Install only the Linux version via "ARM GCC TOOLS"->"GNU ARM Embedded Toolchain 9-2019-q4-major for Linux"
    - Press through via "Next" and accept the license agreement
    - Wait for the "Installing Software: XY%" indicator in the bottom right of the Eclipse GUI to finish
    - Wait for the "Restart" window to pop up and restart Eclipse
    - In case Updates are available, install all updates and restart the IDE

1. Download the SimpleLink SDK and extract to "~/ti"
```shell
mkdir -p ~/ti && run wget -O sdk.zip --progress=dot:giga https://dr-download.ti.com/software-development/software-development-kit-sdk/MD-BPlR3djvTV/7.41.00.17/simplelink_cc13xx_cc26xx_sdk_7_41_00_17__linux.zip && unzip -q -d ~/ti sdk.zip && rm sdk.zip
```
    - ensure that the exact path now exists: "~/ti/simplelink_cc13xx_cc26xx_sdk_7_41_00_17/examples"
    - Important: The exact locations of the SDK and CCS are important as the generated makefiles will use these exact paths
2. Import an example project from the SDK via
    - File->import->"Code Composer Studio->CCS Projects"->Next->Browse ("Select search-directory")
    - Select the path of the example within the SDK and click "Open", for example: "~/ti/simplelink_cc13xx_cc26xx_sdk_7_41_00_17/examples/nortos/LP_CC1311P3/drivers/uart2echo"
    - Projects should now have been discovered and shown under "discovered projects"
    - Select the desired project and click "Finish"
3. Build and clean project in CCS Gui
    - Right click on project and click "Build Project"
    - Right click on project and click "Clean Project"
    - This will create auto-generated Makefiles in the "Debug" subdirectory of the project
4. Generate the syscfg files
    - Open a terminal for the project: Right click the project and click "Show in Local Terminal"->"Terminal"
    - Within the terminal, run `make -C Debug syscfg`
5. Ensure that the resulting project can now be built using the Docker container
    - Within the docker container from the project directory, run `make -C Debug all`

### Troubleshooting Building in Docker

The paths expected by the CCS-generated build scripts need to be valid within the Docker container:
1. GCC within CCS location:
    - See gcc invocation in: `Debug/subdir_rules.mk`
    - Example: `/home/user/ti/ccs1271/ccs/tools/compiler/gcc-arm-none-eabi-9-2019-q4-major/bin/arm-none-eabi-gcc-9.2.1`
    - -> Check that this directory exists within the build docker container
2. SDK location:
    - See include directories containing "simplelink" in gcc invocation in `Debug/subdir_rules.mk`
    - Example: `-I"/home/user/ti/simplelink_cc13xx_cc26xx_sdk_7_41_00_17/source"`
    - -> Check that this directory exists within the build docker container
3. Project location: /home/user/TI-CCS-workspace_v12/empty_LP_CC1311P3_nortos_gcc
    - See include directories containing the project name in gcc invocation in `Debug/subdir_rules.mk`
    - Example: `-I"/home/user/TI-CCS-workspace_v12/empty_LP_CC1311P3_nortos_gcc"`
    - -> Check that this directory exists within the build docker container

In case these paths do not exist, check the following:
1. The Code Composer Studio version leading to a different installation path
    - Add symlink to updated CCS version: `/home/user/ti/ccs<MY_NEW_CCS_VERSION>/ccs/tools/compiler/gcc-arm-none-eabi-9-2019-q4-major/bin/arm-none-eabi-gcc-9.2.1`
2. SDK Version changes
    - Add symlink to updated SDK version: `/home/user/ti/simplelink_cc13xx_cc26xx_sdk_<MY_NEW_SDK_VERSION>`
