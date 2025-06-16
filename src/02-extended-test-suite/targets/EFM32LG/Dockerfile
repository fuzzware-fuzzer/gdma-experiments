# password-base has a compiler and some utilities such as wget and unzip
FROM password-base 
RUN apt update; apt install -y openjdk-21-jdk
# we need the sdk for all samples because of the relative path, so install it here
RUN mkdir -p /home/ubuntu/silabs-new/
WORKDIR /home/ubuntu/silabs-new/
RUN wget https://www.silabs.com/documents/login/software/slc_cli_linux.zip 
RUN unzip slc_cli_linux.zip
RUN git clone https://github.com/SiliconLabs/gecko_sdk.git --branch v4.4.4

# build the samples
CMD ["/bin/bash","/opt/samples/build_samples.sh"]
