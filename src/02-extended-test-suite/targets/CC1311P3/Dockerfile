from ubuntu:20.04

run apt-get update && apt-get install -y wget unzip build-essential

env GCC_PATH=/gcc-arm-none-eabi-9-2019-q4-major
env CCS_INSTALL_PATH=/home/user/ti/ccs
env TI_SIMPLELINK_SDK_VER=simplelink_cc13xx_cc26xx_sdk_7_41_00_17
env SHARE_PATH=/opt/samples

# Install arm-none-eabi-gcc (gcc-arm-none-eabi-9-2019-q4-major)
run wget -O gcc.tar.bz2 --progress=dot:giga https://developer.arm.com/-/media/Files/downloads/gnu-rm/9-2019q4/gcc-arm-none-eabi-9-2019-q4-major-x86_64-linux.tar.bz2 && tar -xf gcc.tar.bz2 --directory / && rm gcc.tar.bz2

# Set up directories and Links as we expect the VM to be set up (CCS, SDK and the workspace)
run mkdir -p /home/user/ti "${CCS_INSTALL_PATH}/ccs/tools/compiler"
# GCC in CCS tool path
run ln -s "${GCC_PATH}" "${CCS_INSTALL_PATH}/ccs/tools/compiler"
# Link default workspace location
run ln -s "${SHARE_PATH}" /home/user/ti/workspace

# Install SDK to /home/user/ti
run wget -O sdk.zip --progress=dot:giga https://dr-download.ti.com/software-development/software-development-kit-sdk/MD-BPlR3djvTV/7.41.00.17/${TI_SIMPLELINK_SDK_VER}__linux.zip && unzip -q -d /home/user/ti sdk.zip && rm sdk.zip

workdir "${SHARE_PATH}"
CMD ["/bin/bash","/opt/samples/build_samples.sh"]
