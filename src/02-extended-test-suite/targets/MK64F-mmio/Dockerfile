# password-base has a compiler and some utilities such as wget and unzip
FROM password-base 

# we need the sdk for all samples because of the relative path, so install it here
WORKDIR /opt
# great, I love docker because we can just destroy the local python packages
RUN pip install --user west --break-system-packages
RUN PATH=$PATH:/root/.local/bin west init -m https://github.com/NXPmicro/mcux-sdk mcuxsdk --mr MCUX_2.16.100
WORKDIR /opt/mcuxsdk
RUN PATH=$PATH:/root/.local/bin west update
# default print debug uses 115200, change to 9600
RUN sed -i "s/#define BOARD_DEBUG_UART_BAUDRATE 115200/#define BOARD_DEBUG_UART_BAUDRATE 9600/g" core/boards/frdmk64f/board.h
# build the samples
CMD ["/bin/bash","/opt/samples/build_samples.sh"]
