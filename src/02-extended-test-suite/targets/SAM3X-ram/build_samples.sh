sample1_dir="/opt/samples/sam3x_uart_scatter/USART_USART_DMAC_EXAMPLE1/Debug"
sample1_output="USART_USART_DMAC_EXAMPLE1.elf"
sample1_final_name="sam3x_uart_scatter.elf"

export PATH=$PATH:/opt/compiler/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin
mkdir /opt/samples/output
cd $sample1_dir; ln -s ../src/ . ; make clean; make all; cp $sample1_output /opt/samples/output/$sample1_final_name
