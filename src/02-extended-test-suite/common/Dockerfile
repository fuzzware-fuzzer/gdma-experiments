FROM ubuntu:24.04

RUN apt-get update
RUN apt-get install -y make wget xz-utils unzip git cmake python3 python3-pip

WORKDIR "/opt"
RUN mkdir compiler
WORKDIR "/opt/compiler"
RUN wget https://developer.arm.com/-/media/Files/downloads/gnu/13.2.rel1/binrel/arm-gnu-toolchain-13.2.rel1-x86_64-arm-none-eabi.tar.xz
RUN tar -xf arm-gnu-toolchain-13.2.rel1-x86_64-arm-none-eabi.tar.xz
