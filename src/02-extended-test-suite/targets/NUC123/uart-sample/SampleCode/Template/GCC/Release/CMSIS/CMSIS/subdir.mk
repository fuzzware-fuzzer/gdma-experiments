################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
/home/ubuntu/NUC123BSP/Library/Device/Nuvoton/NUC123/Source/system_NUC123.c 

OBJS += \
./CMSIS/CMSIS/system_NUC123.o 

C_DEPS += \
./CMSIS/CMSIS/system_NUC123.d 


# Each subdirectory must supply rules for building sources it contributes
CMSIS/CMSIS/system_NUC123.o: /home/ubuntu/NUC123BSP/Library/Device/Nuvoton/NUC123/Source/system_NUC123.c CMSIS/CMSIS/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


