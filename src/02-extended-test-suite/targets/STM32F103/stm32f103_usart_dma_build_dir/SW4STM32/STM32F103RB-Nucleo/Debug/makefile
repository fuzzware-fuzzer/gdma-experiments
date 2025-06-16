################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (12.3.rel1)
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include Example/User/subdir.mk
-include Example/SW4STM32/subdir.mk
-include Drivers/STM32F1xx_LL_Driver/subdir.mk
-include Drivers/CMSIS/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

OPTIONAL_TOOL_DEPS := \
$(wildcard ../makefile.defs) \
$(wildcard ../makefile.init) \
$(wildcard ../makefile.targets) \


BUILD_ARTIFACT_NAME := STM32F103RB-Nucleo
BUILD_ARTIFACT_EXTENSION := elf
BUILD_ARTIFACT_PREFIX :=
BUILD_ARTIFACT := $(BUILD_ARTIFACT_PREFIX)$(BUILD_ARTIFACT_NAME)$(if $(BUILD_ARTIFACT_EXTENSION),.$(BUILD_ARTIFACT_EXTENSION),)

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
STM32F103RB-Nucleo.elf \

MAP_FILES += \
STM32F103RB-Nucleo.map \

SIZE_OUTPUT += \
default.size.stdout \

OBJDUMP_LIST += \
STM32F103RB-Nucleo.list \

OBJCOPY_HEX += \
STM32F103RB-Nucleo.hex \

#CC := /opt/compiler/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-gcc
#OC := /opt/compiler/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-objcopy
#CD := /opt/compiler/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-objdump
#SI := /opt/compiler/arm-gnu-toolchain-13.2.Rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-size

CC := arm-none-eabi-gcc
OC := arm-none-eabi-objcopy
OD := arm-none-eabi-objdump
SI := arm-none-eabi-size
# All Target
all: main-build

# Main-build Target
main-build: STM32F103RB-Nucleo.elf secondary-outputs

# Tool invocations
STM32F103RB-Nucleo.elf STM32F103RB-Nucleo.map: $(OBJS) $(USER_OBJS) ../STM32F103RBTx_FLASH.ld makefile objects.list $(OPTIONAL_TOOL_DEPS)
	$(CC) -o "STM32F103RB-Nucleo.elf" @"objects.list" $(USER_OBJS) $(LIBS) -mcpu=cortex-m3 -T"../STM32F103RBTx_FLASH.ld" --specs=nosys.specs -Wl,-Map="STM32F103RB-Nucleo.map" -Wl,--gc-sections -static --specs=nano.specs -mfloat-abi=soft -mthumb -Wl,--start-group -lc -lm -Wl,--end-group
	@echo 'Finished building target: $@'
	@echo ' '

default.size.stdout: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	$(SI)  $(EXECUTABLES)
	@echo 'Finished building: $@'
	@echo ' '

STM32F103RB-Nucleo.list: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	$(OD) -h -S $(EXECUTABLES) > "STM32F103RB-Nucleo.list"
	@echo 'Finished building: $@'
	@echo ' '

STM32F103RB-Nucleo.hex: $(EXECUTABLES) makefile objects.list $(OPTIONAL_TOOL_DEPS)
	$(OC)  -O ihex $(EXECUTABLES) "STM32F103RB-Nucleo.hex"
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) STM32F103RB-Nucleo.elf STM32F103RB-Nucleo.hex STM32F103RB-Nucleo.list STM32F103RB-Nucleo.map default.size.stdout
	-@echo ' '

secondary-outputs: $(SIZE_OUTPUT) $(OBJDUMP_LIST) $(OBJCOPY_HEX)

fail-specified-linker-script-missing:
	@echo 'Error: Cannot find the specified linker script. Check the linker settings in the build configuration.'
	@exit 2

warn-no-linker-script-specified:
	@echo 'Warning: No linker script specified. Check the linker settings in the build configuration.'

.PHONY: all clean dependents main-build fail-specified-linker-script-missing warn-no-linker-script-specified

-include ../makefile.targets
