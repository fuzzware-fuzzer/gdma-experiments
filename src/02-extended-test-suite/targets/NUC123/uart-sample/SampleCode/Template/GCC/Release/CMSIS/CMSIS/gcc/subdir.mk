################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
/home/ubuntu/NUC123BSP/Library/Device/Nuvoton/NUC123/Source/gcc/_syscalls.c 

S_UPPER_SRCS += \
/home/ubuntu/NUC123BSP/Library/Device/Nuvoton/NUC123/Source/gcc/startup_NUC123.S 

OBJS += \
./CMSIS/CMSIS/gcc/_syscalls.o \
./CMSIS/CMSIS/gcc/startup_NUC123.o 

S_UPPER_DEPS += \
./CMSIS/CMSIS/gcc/startup_NUC123.d 

C_DEPS += \
./CMSIS/CMSIS/gcc/_syscalls.d 


# Each subdirectory must supply rules for building sources it contributes
CMSIS/CMSIS/gcc/_syscalls.o: /home/ubuntu/NUC123BSP/Library/Device/Nuvoton/NUC123/Source/gcc/_syscalls.c CMSIS/CMSIS/gcc/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

CMSIS/CMSIS/gcc/startup_NUC123.o: /home/ubuntu/NUC123BSP/Library/Device/Nuvoton/NUC123/Source/gcc/startup_NUC123.S CMSIS/CMSIS/gcc/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU Assembler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -x assembler-with-cpp -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


