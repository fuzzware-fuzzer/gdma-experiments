FROM ghcr.io/armmbed/mbed-os-env@sha256:302695f5fd9aeb3912f5ed1b9b2e3d6266d9ed8e9c6bfe29f70b77fe20ffced4

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y install python3-venv

# setup clean env
WORKDIR /opt
RUN git clone https://github.com/mbed-ce/mbed-os-example-ble mbed-os
RUN git -C mbed-os/ checkout 711c5ca0ae6ba0253730db9d481b8f1462fd24e9
RUN git -C mbed-os/ submodule set-url mbed-os https://github.com/Diff-fusion/mbed-os
RUN git -C mbed-os/ submodule update --init --no-recommend-shallow
RUN git -C mbed-os/mbed-os/ fetch origin ed371ed04537cd0f01c32af6a069847310bc6cbe
CMD ["/bin/bash","/opt/samples/build_samples.sh"]
	
