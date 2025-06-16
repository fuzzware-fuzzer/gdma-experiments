sample_base_dir="/opt/samples"

sample1_base_dir="$sample_base_dir/uart-sample/"
sample1_dir="SampleCode/Template/GCC/Release"
sample1_output="Template.elf"
sample1_final_name="nuc123_uart_example.elf"

base_dir="/home/ubuntu/NUC123BSP"
out_dir="/opt/samples/output"
export PATH=$PATH:/opt/compiler/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin

# create output directory
mkdir $out_dir 

# create expected hardcoded paths
mkdir -p $base_dir 
# move files to expected position
mv $sample1_base_dir/Library $base_dir 
mv $sample1_base_dir/SampleCode $base_dir 

## Build sample 1
# go to correct directory
cd $base_dir/SampleCode/Template/GCC/Release
# build the thing
make all
# copy binary to output dir for later pickup
cp $sample1_output $out_dir/$sample1_final_name 
