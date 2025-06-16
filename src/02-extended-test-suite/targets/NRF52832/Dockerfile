# password-base has a compiler and some utilities such as wget and unzip
FROM password-base 

# we need the sdk for all samples because of the relative path, so install it here
RUN mkdir -p /opt/sdk
WORKDIR /opt/sdk
RUN wget https://nsscprodmedia.blob.core.windows.net/prod/software-and-other-downloads/sdks/nrf5/binaries/nrf5_sdk_17.1.0_ddde560.zip
RUN unzip nrf5_sdk_17.1.0_ddde560.zip
RUN sed -i s+/usr/local/gcc-arm-none-eabi-9-2020-q2-update/bin/+/opt/compiler/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin/+ /opt/sdk/nRF5_SDK_17.1.0_ddde560/components/toolchain/gcc/Makefile.posix

# build the samples
CMD ["/bin/bash","/opt/samples/build_samples.sh"]
