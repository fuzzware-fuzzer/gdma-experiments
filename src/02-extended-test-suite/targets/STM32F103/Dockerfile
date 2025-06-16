FROM password-base 

RUN cd /opt/ &&\
git clone --recursive  --depth 1 --branch v1.8.5 https://github.com/STMicroelectronics/STM32CubeF1.git &&\
cd STM32CubeF1 &&\
git pull &&\
git submodule update --init --recursive &&\
cd -

CMD ["/bin/bash","/opt/samples/build_samples.sh"]
