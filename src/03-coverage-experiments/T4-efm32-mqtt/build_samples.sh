sample_base_dir="/opt/samples"

base_dir="/home/ubuntu/silabs-new/"
out_dir="/opt/samples/output"

# create output directory
mkdir $out_dir 

# create expected hardcoded paths
mkdir -p $base_dir 

cd $base_dir
# COPY updated uart baremetal config and source files
cp /opt/samples/projects/uartdrv_baremetal.slcp /home/ubuntu/silabs-new/gecko_sdk/app/common/example/uartdrv_baremetal/
cp /opt/samples/projects/buffer.c /home/ubuntu/silabs-new/gecko_sdk/app/common/example/uartdrv_baremetal
cp /opt/samples/projects/buffer.h /home/ubuntu/silabs-new/gecko_sdk/app/common/example/uartdrv_baremetal
cp /opt/samples/projects/errors.c /home/ubuntu/silabs-new/gecko_sdk/app/common/example/uartdrv_baremetal
cp /opt/samples/projects/errors.h /home/ubuntu/silabs-new/gecko_sdk/app/common/example/uartdrv_baremetal
cp /opt/samples/projects/message.c /home/ubuntu/silabs-new/gecko_sdk/app/common/example/uartdrv_baremetal
cp /opt/samples/projects/message.h /home/ubuntu/silabs-new/gecko_sdk/app/common/example/uartdrv_baremetal
cp /opt/samples/projects/parser.c /home/ubuntu/silabs-new/gecko_sdk/app/common/example/uartdrv_baremetal
cp /opt/samples/projects/parser.h /home/ubuntu/silabs-new/gecko_sdk/app/common/example/uartdrv_baremetal
cp /opt/samples/projects/serialiser.c /home/ubuntu/silabs-new/gecko_sdk/app/common/example/uartdrv_baremetal
cp /opt/samples/projects/serialiser.h /home/ubuntu/silabs-new/gecko_sdk/app/common/example/uartdrv_baremetal


./slc_cli/slc configuration --sdk=gecko_sdk/gecko_sdk.slcs
./slc_cli/slc signature trust --sdk gecko_sdk/gecko_sdk.slcs
./slc_cli/slc configuration --gcc-toolchain=/opt/compiler/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/
./slc_cli/slc generate gecko_sdk/app/common/example/uartdrv_baremetal/uartdrv_baremetal.slcp -np -d=proj/ -name=test --with brd2001a
cd proj
cp /opt/samples/projects/uartdrv_app.c .
cp /opt/samples/projects/sl_uartdrv_leuart_vcom_config.h config
cp /opt/samples/projects/pw_check.h .



make -f test.Makefile
cp /home/ubuntu/silabs-new/proj/build/debug/test.out /home/ubuntu/silabs-new/proj/build/debug/test.elf
cp /home/ubuntu/silabs-new/proj/build/debug/test.elf $out_dir
