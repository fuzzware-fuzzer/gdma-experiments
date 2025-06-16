FROM docker.io/zephyrprojectrtos/zephyr-build:v0.27.4
# workspace_dir=/workdir/workspace-$ZEPHYR_VERSION

RUN sudo mkdir /opt/zephyr
RUN sudo chmod 777 /opt/zephyr
RUN west init --mr=zephyr-v3.5.0 /opt/zephyr
WORKDIR /opt/zephyr 
RUN west update
WORKDIR /opt/zephyr/zephyr
# export ZEPHYR_BASE=$(pwd)

# Restore git state
RUN git reset --hard
RUN git clean -df
RUN git checkout v3.5.0
RUN west update

CMD ["/bin/bash","/opt/samples/build_samples.sh"]
