sample1_final_name="stm32f103_usart_contiguous.elf"

export PATH=$PATH:/opt/compiler/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin
rm -r /opt/STM32CubeF1/Projects/STM32F103RB-Nucleo/Examples_LL/USART/USART_Communication_TxRx_DMA/*
mv /opt/samples/stm32f103_usart_dma_build_dir/* /opt/STM32CubeF1/Projects/STM32F103RB-Nucleo/Examples_LL/USART/USART_Communication_TxRx_DMA/
cd /opt/STM32CubeF1/Projects/STM32F103RB-Nucleo/Examples_LL/USART/USART_Communication_TxRx_DMA/SW4STM32/STM32F103RB-Nucleo/Debug
make clean 
make all
mkdir -p /opt/samples/output
cp STM32F103RB-Nucleo.elf /opt/samples/output/$sample1_final_name
