FROM ubuntu:18.04
WORKDIR /opt

ENV IDE_VERSION 11.10.0_3148

COPY ./mcuxpressoide-${IDE_VERSION}.x86_64.deb.bin /opt


# Install any needed packages specified in requirements.txt
RUN apt update && \
    apt upgrade -y && \
    apt install -y \
# Development files
      whiptail \
      build-essential \
      bzip2 \
      libswt-gtk-3-jni \
      libswt-gtk-3-java \
      unzip \
      wget && \
    apt clean

# install mcuxpresso
RUN chmod a+x mcuxpressoide-${IDE_VERSION}.x86_64.deb.bin &&\
  # Extract the installer to a deb package
  ./mcuxpressoide-${IDE_VERSION}.x86_64.deb.bin --noexec --target mcu --keep &&\
  cd mcu &&\
  dpkg --add-architecture i386 && apt-get update &&\
  apt-get install -y libusb-1.0-0-dev dfu-util libwebkitgtk-1.0-0 libncurses5:i386 udev &&\
  #dpkg --force-depends -i JLink_Linux_x86_64.deb &&\
  dpkg --unpack JLink_Linux_x86_64.deb &&\
  rm -f /var/lib/dpkg/info/jlink.postinst &&\
  dpkg --force-depends --configure jlink &&\
  #apt install -yf &&\
  # manually install mcuxpressoide - post install script fails
  dpkg --unpack mcuxpressoide-${IDE_VERSION}.x86_64.deb &&\
  rm /var/lib/dpkg/info/mcuxpressoide.postinst -f &&\
  dpkg --configure mcuxpressoide &&\
  apt-get install -yf &&\
  # manually run the postinstall script
  mkdir -p /usr/share/NXPLPCXpresso &&\
  chmod a+w /usr/share/NXPLPCXpresso &&\
  ln -s /usr/local/mcuxpressoide-${IDE_VERSION} /usr/local/mcuxpressoide
ENV TOOLCHAIN_PATH /usr/local/mcuxpressoide/ide/tools/bin
ENV PATH $TOOLCHAIN_PATH:$PATH

## install linkserver
RUN chmod a+x /usr/local/mcuxpressoide/LinkServer*.deb.bin 
RUN /usr/local/mcuxpressoide/LinkServer*.deb.bin acceptLicense

# add the sdk package
RUN mkdir -p /root/mcuxpresso/02/SDKPackages
RUN rm mcuxpressoide-${IDE_VERSION}.x86_64.deb.bin
RUN rm -rf mcu
CMD ["/bin/bash","/opt/samples/build_samples.sh"]
