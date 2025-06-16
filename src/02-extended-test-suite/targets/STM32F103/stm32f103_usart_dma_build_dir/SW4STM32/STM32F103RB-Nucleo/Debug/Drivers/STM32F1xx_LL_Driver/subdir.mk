################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
/opt/STM32CubeF1/Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_ll_utils.c 

OBJS += \
./Drivers/STM32F1xx_LL_Driver/stm32f1xx_ll_utils.o 

C_DEPS += \
./Drivers/STM32F1xx_LL_Driver/stm32f1xx_ll_utils.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/STM32F1xx_LL_Driver/stm32f1xx_ll_utils.o: /opt/STM32CubeF1/Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_ll_utils.c Drivers/STM32F1xx_LL_Driver/subdir.mk
	$(CC) "$<" -mcpu=cortex-m3 -std=gnu11 -g3 -DSTM32F103xB -DUSE_FULL_LL_DRIVER -c -I../../../Inc -I../../../../../../../../Drivers/CMSIS/Device/ST/STM32F1xx/Include -I../../../../../../../../Drivers/STM32F1xx_HAL_Driver/Inc -I../../../../../../../../Drivers/CMSIS/Include -Os -ffunction-sections -Wall -fstack-usage -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfloat-abi=soft -mthumb -o "$@"

clean: clean-Drivers-2f-STM32F1xx_LL_Driver

clean-Drivers-2f-STM32F1xx_LL_Driver:
	-$(RM) ./Drivers/STM32F1xx_LL_Driver/stm32f1xx_ll_utils.cyclo ./Drivers/STM32F1xx_LL_Driver/stm32f1xx_ll_utils.d ./Drivers/STM32F1xx_LL_Driver/stm32f1xx_ll_utils.o ./Drivers/STM32F1xx_LL_Driver/stm32f1xx_ll_utils.su

.PHONY: clean-Drivers-2f-STM32F1xx_LL_Driver

