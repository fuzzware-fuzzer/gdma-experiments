FROM ubuntu:24.04

RUN apt-get update && apt-get -y install \
    git build-essential perl python3 \
    libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxkbcommon-x11-0 libglib2.0-0 libglx-dev libopengl0 libglu1-mesa-dev libegl1 libdbus-1-dev

COPY ModusToolbox_3.2.0.16028-linux-install.deb /tmp/
RUN dpkg -i /tmp/ModusToolbox_3.2.0.16028-linux-install.deb

WORKDIR /data
CMD ["/bin/bash","/opt/samples/build_samples.sh"]
# RUN /opt/Tools/ModusToolbox/tools_3.2/project-creator/project-creator-cli --board-id CY8CKIT-062-BLE --app-id mtb-example-psoc6-uart-transmit-receive-dma --target-dir /data
# 
# WORKDIR /data/mtb-example-psoc6-uart-transmit-receive-dma
# 
# RUN sed -i 's;CY_TOOLS_PATHS+=;CY_TOOLS_PATHS+=/opt/Tools/ModusToolbox/tools_3.2;' Makefile
# 
# COPY password.patch ./
# RUN patch -p1 < password.patch
# 
# RUN make getlibs
# RUN make build -j
