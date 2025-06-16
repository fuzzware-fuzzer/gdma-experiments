
DIR="/opt/samples"
whoami 
id
groups
cd /opt/contiki-ng
# disable soft float for fuzzware
git apply $DIR/patches/soft_float.patch

# enable debug info
git apply $DIR/patches/debug_info.patch

rm -rf /opt/contiki-ng/examples/hello-world/build
make -j -C /opt/contiki-ng/examples/hello-world TARGET=nrf BOARD=nrf52840/dongle clean all
# Copy sample to outside-visible directory
cp /opt/contiki-ng/examples/hello-world/build/nrf/nrf52840/dongle/hello-world.elf /opt/samples/output
