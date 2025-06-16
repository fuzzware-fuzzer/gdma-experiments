FROM ubuntu:22.04

RUN apt-get update
RUN apt-get install -y make wget xz-utils unzip git cmake python3 python3-pip curl automake texinfo coreutils 

WORKDIR "/opt"
RUN mkdir -p "/opt/DICE-DMA-Emulation"
COPY DICE-DMA-Emulation /opt/DICE-DMA-Emulation
RUN mkdir -p "/opt/P2IM-DMA-Emulation"
COPY p2im_dice/DICE-DMA-Emulation /opt/P2IM-DMA-Emulation

RUN mkdir -p tools
RUN cd tools && wget https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-x86_64-arm-none-eabi.tar.xz && tar -xf arm-gnu-toolchain-13.2.rel1-x86_64-arm-none-eabi.tar.xz
ENV PATH="$PATH:/opt/tools/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin/"

# Copy configs for fuzzing
RUN mkdir -p "/opt/p2im_configs"
COPY p2im_configs /opt/p2im_configs

RUN mkdir -p "/opt/dice_configs"
COPY dice_configs /opt/dice_configs

RUN mkdir -p "/opt/scripts"
COPY ./scripts/* /opt/scripts/

