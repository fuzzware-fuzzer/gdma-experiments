FROM password-base 

#RUN apt-get -y install gcc-arm-linux-gnueabihf
WORKDIR /opt/
RUN git clone https://github.com/Mbed-TLS/mbedtls.git && cd mbedtls && git checkout f4f37eced7c39db5db4c6b5c5c6ec98bd81fe416
CMD ["/bin/bash","/opt/samples/build_samples.sh"]
