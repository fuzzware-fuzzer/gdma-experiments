# STM32F10 USART password sample

## Prerequisites
None

## Building
TLDR: Just execute the build docker script  
More detailed:
- Sample is based on the USART Communication TxRx DMA sample from the [STM32CubeF1 Repository](https://github.com/STMicroelectronics/STM32CubeF1)
- Patches to the main function are detailed in the [patch file](./main.patch)
- Additionally, the [pw\_check.h](./stm32f103_usart_dma_build_dir/Src/pw_check.h) is added
- For ease of building all target-specific files are collected in `stm32f103_usart_dma_build_dir`

## Adding a new STM32F103 sample
Sadly the STM32CubeF1 repository does not provide Makefiles and such. 
Instead we used the [Open STM32 System Workbench](https://www.openstm32.org/Downloading%2Bthe%2BSystem%2BWorkbench%2Bfor%2BSTM32%2Binstaller) to import projects from the cloned github and create valid Makefiles. 
We then copied the entire directory setup by the System workbench into the Docker and compile them there.
