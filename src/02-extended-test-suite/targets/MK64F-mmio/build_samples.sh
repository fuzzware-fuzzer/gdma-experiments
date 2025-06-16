sample_base_dir="/opt/samples"

sample1_base_dir="$sample_base_dir/uart-sample/"
sample1_output="debug/uart_edma_transfer.elf"
sample1_final_name="uart_example.elf"

sdk_base_dir="/opt/mcuxsdk/"
out_dir="/opt/samples/output"
# export PATH=$PATH:/opt/compiler/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin
export ARMGCC_DIR=/opt/compiler/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi
# copy projects to correct sdk location
cp -r $sample1_base_dir/uart_edma_transfer.c $sdk_base_dir/examples/frdmk64f/driver_examples/uart/edma_transfer
cp -r $sample1_base_dir/pw_check.h $sdk_base_dir/examples/frdmk64f/driver_examples/uart/edma_transfer

# create output directory
mkdir $out_dir 

## Build sample 1
# go to correct directory
cd $sdk_base_dir/examples/frdmk64f/driver_examples/uart/edma_transfer/armgcc
# build the thing
sh build_all.sh
# copy binary to output dir for later pickup
cp $sample1_output $out_dir/$sample1_final_name 
