FROM ubuntu:24.04

ENV ARMGCC_DIR=/usr
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && \
	apt-get -y upgrade && \
	apt-get install --no-install-recommends -y \
    cmake \
    make \
    gcc-arm-none-eabi \
    libnewlib-arm-none-eabi \
    git \
    python3-venv \
	&& \
    apt-get clean -y && \
	apt-get autoremove --purge -y && \
	rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install west
WORKDIR /opt
RUN west init -m https://github.com/NXPmicro/mcux-sdk --mr MCUX_2.16.100 "mcuxsdk"
WORKDIR /opt/mcuxsdk
RUN west update
WORKDIR /opt/mcuxsdk/core
RUN git reset --hard
RUN git clean -df
RUN git checkout MCUX_2.16.100
RUN west update
CMD ["/bin/bash","/opt/samples/build_samples.sh"]
