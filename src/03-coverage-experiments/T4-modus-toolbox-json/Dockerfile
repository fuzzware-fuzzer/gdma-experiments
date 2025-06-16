FROM ubuntu:24.04

RUN apt-get update && apt-get -y install \
    git build-essential perl python3 \
    libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxkbcommon-x11-0 libglib2.0-0 libglx-dev libopengl0 libglu1-mesa-dev libegl1 libdbus-1-dev

COPY ModusToolbox_3.2.0.16028-linux-install.deb /tmp/
RUN dpkg -i /tmp/ModusToolbox_3.2.0.16028-linux-install.deb
CMD ["/bin/bash","/opt/samples/build_samples.sh"]
