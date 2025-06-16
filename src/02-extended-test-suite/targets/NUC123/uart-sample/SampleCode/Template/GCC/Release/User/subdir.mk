################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
/home/ubuntu/NUC123BSP/SampleCode/Template/main.c 

OBJS += \
./User/main.o 

C_DEPS += \
./User/main.d 


# Each subdirectory must supply rules for building sources it contributes
User/main.o: /home/ubuntu/NUC123BSP/SampleCode/Template/main.c User/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


