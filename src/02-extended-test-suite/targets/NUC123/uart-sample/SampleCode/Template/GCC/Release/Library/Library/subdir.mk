################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/adc.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/clk.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/crc.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/fmc.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/gpio.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/i2c.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/pdma.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/pwm.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/retarget.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/spi.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/sys.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/timer.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/uart.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/usbd.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/wdt.c \
/home/ubuntu/NUC123BSP/Library/StdDriver/src/wwdt.c 

OBJS += \
./Library/Library/adc.o \
./Library/Library/clk.o \
./Library/Library/crc.o \
./Library/Library/fmc.o \
./Library/Library/gpio.o \
./Library/Library/i2c.o \
./Library/Library/pdma.o \
./Library/Library/pwm.o \
./Library/Library/retarget.o \
./Library/Library/spi.o \
./Library/Library/sys.o \
./Library/Library/timer.o \
./Library/Library/uart.o \
./Library/Library/usbd.o \
./Library/Library/wdt.o \
./Library/Library/wwdt.o 

C_DEPS += \
./Library/Library/adc.d \
./Library/Library/clk.d \
./Library/Library/crc.d \
./Library/Library/fmc.d \
./Library/Library/gpio.d \
./Library/Library/i2c.d \
./Library/Library/pdma.d \
./Library/Library/pwm.d \
./Library/Library/retarget.d \
./Library/Library/spi.d \
./Library/Library/sys.d \
./Library/Library/timer.d \
./Library/Library/uart.d \
./Library/Library/usbd.d \
./Library/Library/wdt.d \
./Library/Library/wwdt.d 


# Each subdirectory must supply rules for building sources it contributes
Library/Library/adc.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/adc.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/clk.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/clk.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/crc.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/crc.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/fmc.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/fmc.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/gpio.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/gpio.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/i2c.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/i2c.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/pdma.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/pdma.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/pwm.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/pwm.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/retarget.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/retarget.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/spi.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/spi.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/sys.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/sys.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/timer.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/timer.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/uart.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/uart.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/usbd.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/usbd.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/wdt.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/wdt.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

Library/Library/wwdt.o: /home/ubuntu/NUC123BSP/Library/StdDriver/src/wwdt.c Library/Library/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: Cross ARM GNU C Compiler'
	arm-none-eabi-gcc -mcpu=cortex-m0 -mthumb -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections  -g -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/CMSIS/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/Device/Nuvoton/NUC123/Include" -I"/home/ubuntu/NUC123BSP/SampleCode/Template/GCC/../../../Library/StdDriver/inc" -I/home/ubuntu/NUC123BSP/SampleCode/Template/GCC -std=gnu11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -c -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


