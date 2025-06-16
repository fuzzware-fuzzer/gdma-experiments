FROM cptquooker/docker_e2studio_2024-04
RUN apt-get update && apt-get install --yes wget unzip git
WORKDIR /opt/samples/picohttpparser
RUN mkdir -p /tmp/fsp \
    && cd /tmp/fsp \
    && wget https://github.com/renesas/fsp/releases/download/v5.4.0/FSP_Packs_v5.4.0.zip \
    && unzip FSP_Packs_v5.4.0.zip \
    && cp -r internal/* /opt/e2studio/internal \
    && cd / \
    && rm -rf /tmp/fsp
CMD ["/bin/bash","/opt/samples/build_samples.sh"]
