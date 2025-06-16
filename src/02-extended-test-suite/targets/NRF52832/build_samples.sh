sample_base_dir="/opt/samples"

sample1_base_dir="$sample_base_dir/uart_example/"
sample1_dir="uart_example/pca10040/blank/armgcc"
sample1_output="_build/nrf52832_xxaa.out"
sample1_final_name="uart_example.elf"

sdk_base_dir="/opt/sdk/nRF5_SDK_17.1.0_ddde560/"
out_dir="/opt/samples/output"
export PATH=$PATH:/opt/compiler/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin

# copy projects to correct sdk location
cp -r $sample1_base_dir $sdk_base_dir/examples/peripheral/

# create output directory
mkdir $out_dir 

## Build sample 1
# go to correct directory
cd $sdk_base_dir/examples/peripheral/$sample1_dir
# remove -Wall which prevents compilation
sed -i s/-Wall// Makefile
# build the thing
make
# copy binary to output dir for later pickup
cp $sample1_output $out_dir/$sample1_final_name 
