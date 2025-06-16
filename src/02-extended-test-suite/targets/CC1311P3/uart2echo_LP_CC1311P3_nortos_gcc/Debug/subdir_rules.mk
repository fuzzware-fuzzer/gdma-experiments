################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: GNU Compiler'
	"/home/user/ti/ccs/ccs/tools/compiler/gcc-arm-none-eabi-9-2019-q4-major/bin/arm-none-eabi-gcc-9.2.1" -c -mcpu=cortex-m4 -march=armv7e-m -mthumb -mfloat-abi=soft -I"/home/user/ti/workspace/uart2echo_LP_CC1311P3_nortos_gcc" -I"/home/user/ti/workspace/uart2echo_LP_CC1311P3_nortos_gcc/Debug" -I"/home/user/ti/simplelink_cc13xx_cc26xx_sdk_7_41_00_17/source" -I"/home/user/ti/simplelink_cc13xx_cc26xx_sdk_7_41_00_17/kernel/nortos" -I"/home/user/ti/simplelink_cc13xx_cc26xx_sdk_7_41_00_17/kernel/nortos/posix" -I"/home/user/ti/ccs/ccs/tools/compiler/gcc-arm-none-eabi-9-2019-q4-major/arm-none-eabi/include/newlib-nano" -I"/home/user/ti/ccs/ccs/tools/compiler/gcc-arm-none-eabi-9-2019-q4-major/arm-none-eabi/include" -O3 -ffunction-sections -fdata-sections -g -gdwarf-3 -gstrict-dwarf -Wall -MMD -MP -MF"$(basename $(<F)).d_raw" -MT"$(@)" -I"/home/user/ti/workspace/uart2echo_LP_CC1311P3_nortos_gcc/Debug/syscfg" -std=c99 $(GEN_OPTS__FLAG) -o"$@" "$(shell echo $<)"
	@echo 'Finished building: "$<"'
	@echo ' '

syscfg/ti_devices_config.c: build-1548991889
syscfg/ti_drivers_config.c: build-1548991889
syscfg/ti_drivers_config.h: build-1548991889
syscfg/ti_utils_build_linker.cmd.genlibs: build-1548991889
syscfg/ti_utils_build_compiler.opt: build-1548991889
syscfg/syscfg_c.rov.xs: build-1548991889
syscfg: build-1548991889

syscfg/%.o: ./syscfg/%.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: GNU Compiler'
	"/home/user/ti/ccs/ccs/tools/compiler/gcc-arm-none-eabi-9-2019-q4-major/bin/arm-none-eabi-gcc-9.2.1" -c -mcpu=cortex-m4 -march=armv7e-m -mthumb -mfloat-abi=soft -I"/home/user/ti/workspace/uart2echo_LP_CC1311P3_nortos_gcc" -I"/home/user/ti/workspace/uart2echo_LP_CC1311P3_nortos_gcc/Debug" -I"/home/user/ti/simplelink_cc13xx_cc26xx_sdk_7_41_00_17/source" -I"/home/user/ti/simplelink_cc13xx_cc26xx_sdk_7_41_00_17/kernel/nortos" -I"/home/user/ti/simplelink_cc13xx_cc26xx_sdk_7_41_00_17/kernel/nortos/posix" -I"/home/user/ti/ccs/ccs/tools/compiler/gcc-arm-none-eabi-9-2019-q4-major/arm-none-eabi/include/newlib-nano" -I"/home/user/ti/ccs/ccs/tools/compiler/gcc-arm-none-eabi-9-2019-q4-major/arm-none-eabi/include" -O3 -ffunction-sections -fdata-sections -g -gdwarf-3 -gstrict-dwarf -Wall -MMD -MP -MF"syscfg/$(basename $(<F)).d_raw" -MT"$(@)" -I"/home/user/ti/workspace/uart2echo_LP_CC1311P3_nortos_gcc/Debug/syscfg" -std=c99 $(GEN_OPTS__FLAG) -o"$@" "$(shell echo $<)"
	@echo 'Finished building: "$<"'
	@echo ' '


