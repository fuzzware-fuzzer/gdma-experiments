mkdir /data
cd /data
/opt/Tools/ModusToolbox/tools_3.2/project-creator/project-creator-cli --board-id CY8CKIT-062-BLE --app-id mtb-example-psoc6-uart-transmit-receive-dma --target-dir /data
cd /data/mtb-example-psoc6-uart-transmit-receive-dma
sed -i 's;CY_TOOLS_PATHS+=;CY_TOOLS_PATHS+=/opt/Tools/ModusToolbox/tools_3.2;' Makefile

patch -p1 < /opt/samples/json.patch

make getlibs
make build -j
cp /data/mtb-example-psoc6-uart-transmit-receive-dma/build/APP_CY8CKIT-062-BLE/Debug/mtb-example-psoc6-uart-transmit-receive-dma.elf /opt/samples/output/
