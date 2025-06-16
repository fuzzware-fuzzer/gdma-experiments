# Analysis of DICE DMA Firmware Targets

This document contains the details of the DMA usage of the different targets in this directory. First there is a template of how the analysis of a new target can be structured, then the already documented targets follow.

| Target                                       | Board      | Doc State |
| -----------                                  | -----      | ----- |
| [GPS-Receiver](#target-gps-receiver)         | STM32F103  | &check; |
| [Guitar-Pedal](#target-guitar-pedal)         | STM32F303  | &check; |
| [MIDI-Synthesizer](#target-midi-synthesizer) | STM32F429  | &check; |
| [Modbus](#target-modbus)                     | STM32F303  | &check; |
| [Soldering-Station](#target-soldering-station)  | STM32F103  | &check; |
| [Stepper-Motor](#target-stepper-motor)       | STM32F466  | &check; |


# Target: Template

DMA Summary: `<Keywords about mechanism>`

Sources:
- https://github.com/RiS3-Lab/DICE-DMA-Emulation/tree/master/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/TODO
- Sources linked in paper: TODO

Known DICE firmware patches:

## Milestones
Successful Processing: 0xADDR (`TODO` case in `function`): [source](TODO)

## Manual Configuration

- Location: 0xdeadbeef (`<symbol>`)
- MMIO address: 0x4000beef (`<MMIO register name>`)
- Size: TODO

## Transfer Mechanism Details
### Thread / Task
**Config**: `<function>` (0xADDR): [source](TODO)

**Task / Loop**: `<function>` (0xADDR)
- **HW Activation**: `<function>` called from `<function>` (0xADDR)
- **Sync Mechanism**: `<semaphore/polling>` -> `<function>` (0xADDR) on variable `<TODO: global name / variable name / ...>`
- **Processing**: `<function>`, ...

### Interrupt Handlers

- **IRQ Handlers**: `<function>` (irq 0x123) / `<function>` (irq 123): [source](TODO)
- **Sync Mechanism**: `<function>` (0xADDR) on variable `<TODO: global name / variable name / ...>`

### Length Handling
- Configured via MMIO register/descriptor field `REGNAME` in `<function>`: [source](TODO)
- Actual size exchanged via global `<varname>`. Set in IRQs (0x0800260c, 0x080025aa), via TODO: constant/MMIO reg
- Check: `<function>` checks `len<TODO`: [src](TODO)


# Target: GPS-Receiver

DMA Summary: RX-only, static buffer, with interrupts setting global flag

Sources:
- https://github.com/RiS3-Lab/DICE-DMA-Emulation/tree/master/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/GPS-Receiver-ST-Workbench
- Sources linked in paper: https://github.com/MaJerle/GPS NMEA parser, https://github.com/MaJerle/STM32 USART DMA

Known DICE firmware patches:
1. Custom synchronization flag setting in [usart_rx_check](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/GPS-Receiver-ST-Workbench/src/main.c#L158-L162) instead of the original [gps_buff_get_full](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/GPS-Receiver-ST-Workbench/src/main.c.bck#L103C11-L103C28)
2. `DMA1_Channel5_IRQHandler` handling of full/half full state ([source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/GPS-Receiver-ST-Workbench/src/main.c#L272-L284))
3. `check_crc` Patched out ([source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/GPS-Receiver-ST-Workbench/src/gps.c#L299))
4. ...

## Milestones

- Reading non-zero input 0x08002026 (`len!=0` case in `gps_process`): [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/GPS-Receiver-ST-Workbench/src/gps.c#L372)
- Matching command `$` in `gps_process`: 0x8001ed2 [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/GPS-Receiver-ST-Workbench/src/gps.c#L373)

## Manual Configuration

- Location: 0x200009d8 (`usart_rx_dma_buffer`)
- MMIO address: 0x40020064 (`LL_DMA_CHANNEL_5->CMAR`) (written at pc `0x80023fe`)
- Size: 0x40

## Transfer Mechanism Details
### Thread / Task
**Config**: `main`->`usart_init`->`LL_DMA_SetMemoryAddress` (0x8002c1e): [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/GPS-Receiver-ST-Workbench/src/main.c#L235C5-L235C28), [HAL Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/GPS-Receiver-ST-Workbench/HAL_Driver/Inc/stm32f1xx_ll_dma.h#L983C66-L983C84)

**Task / Loop**: `main` (0x08002922)
- **HW Activation**: `LL_DMA_EnableChannel` and `LL_USART_Enable` called from `usart_init` (0x08002cb8)
- **Sync Mechanism**: global flag. `main` checks on variable `flag` (0x800293a) [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/GPS-Receiver-ST-Workbench/src/main.c#L100)
- **Processing**: [gps_process](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/GPS-Receiver-ST-Workbench/src/gps.c#L368)

### Interrupt Handlers

- **IRQ Handlers**: `DMA1_Channel5_IRQHandler` (irq 31) / `USART1_IRQHandler` (irq 53): [source](TODO)
- **Sync Mechanism**: `usart_rx_check` on variable `flag`

### Length Handling
- Configured via MMIO register `CNDTR` in `main`->`usart_init`->`LL_DMA_SetDataLength`: [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/GPS-Receiver-ST-Workbench/src/main.c#L236C5-L236C25)
- Actual size exchanged implicitly via `strlen` on buffer
- Check: No check performed





# Target: Guitar-Pedal

DMA Summary: `RX-only buffer, continuous reading, no interrupts`

Sources:
- https://github.com/RiS3-Lab/DICE-DMA-Emulation/tree/master/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Guitar-Pedal-MBED
- Sources linked in paper: [https://github.com/Guitarman9119/Nucleo Guitar Effects Pedal](https://github.com/Guitarman9119/Nucleo_Guitar_Effects_Pedal)

Known DICE firmware patches: 

Spurious Crashes:
- (Early?) interrupts lead to NULL-pointer de-refs. Solved by mapping NULL page or by disabling interrupts (which are not required for DMA in this sample)

## Milestones

Math based on input if-else statement (unknown, which one is harder):
- `080013d4`: > 0.5 case ()
- `080013dc`: == 0.5 case ([source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Guitar-Pedal-MBED/main.cpp#L119))

An interesting case (but not expressible via a single milestone BB is):
fuzzware cov 0x80013dc --exclude 0x080013ba
This case represents the (adc_sample>=0.501) case
The extra filter is required as the basic block 0x80013dc is re-used for control flow if adc_sample==0

## Manual Configuration

- Location: 0x20002af4 (`samps`)
- MMIO address: 0x40020014 (`CMAR`, written at `0x80067b0`)
- Size: 2

## Transfer Mechanism Details
### Thread / Task
**Config**: `ADC1_InitDMA` / `main`->`HAL_ADC_Start_DMA`->`HAL_DMA_Start_IT`->`DMA_SetConfig` (0x80067b0): [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Guitar-Pedal-MBED/main.cpp#L84C5-L84C17)

**Task / Loop**: `main`
- **HW Activation**: No specific per-transfer call, continuous transmissions previously activated in config via `HAL_ADC_Start_DMA`
- **Sync Mechanism**: None, continuous
- **Processing**: `main` reads DMA values from `samps` global, reads button state via MMIO in `button_control`, then reacts in state machine

### Interrupt Handlers

No interrupts used for DMA transfer synchronization.

### Length Handling
- Configured via MMIO register/descriptor field `CNDTR` in `DMA_SetConfig` (Sources not available in main repo)
- Actual size of 2 used implicitly
- Check: No check on size is performed





# Target: MIDI-Synthesizer

DMA Summary: `RX-only buffer, sync via global, interrupts`

Sources:
- https://github.com/RiS3-Lab/DICE-DMA-Emulation/tree/master/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/stm32-codec-midi-mmdsp-test-ST-Workbench
- Sources linked in paper: [https://github.com/mondaugen/stm32-codec-midi-mmdsp-test](https://github.com/mondaugen/stm32-codec-midi-mmdsp-test)

Known DICE firmware patches: MMIO requirements removed in [TIM2_IRQHandler](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/stm32-codec-midi-mmdsp-test-ST-Workbench/src/midi_lowlevel.c#L129)

## Milestones

Seeing byte indicating `MIDIMSG_IS_SYSEX_END` in `MIDIMsgBuilder_update`: 0x08000f2e (`byte == 0xf7` case): [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/stm32-codec-midi-mmdsp-test-ST-Workbench/mmmidi/src/mm_midimsgbuilder.c#L47)

## Manual Configuration

- Location: 0x20004de8 (`midiBuffer`)
- MMIO address: 0x40026094 (`DMA1_Stream5->M0AR`), written at `0x8000288`
- Size: 8 (initialized in struct at `0x80017a6` and written to `NDTR` at `0x8000278`)

## Transfer Mechanism Details
### Thread / Task
**Config**: `main`->`MIDI_low_level_setup_nolib`->`USART2_Enable_Rx`->`DMA_Init` (0x8001614): [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/stm32-codec-midi-mmdsp-test-ST-Workbench/src/main.c#L61), [source setting buffer](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/stm32-codec-midi-mmdsp-test-ST-Workbench/src/midi_lowlevel.c#L52)

**Task / Loop**: `main`
- **HW Activation**: Continuous transmission after config
- **Sync Mechanism**: `polling` -> `MIDI_process_buffer` on variable `MIDITimeToProcessBuffer` [-> src](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/stm32-codec-midi-mmdsp-test-ST-Workbench/src/midi_lowlevel.c#L97)
- **Processing**: `main`->`MIDI_process_buffer`->`MIDI_process_byte`

### Interrupt Handlers

- **IRQ Handlers**: `TIM2_IRQHandler` (irq 44): [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/stm32-codec-midi-mmdsp-test-ST-Workbench/src/midi_lowlevel.c#L130).
- **Sync Mechanism**: `TIM2_IRQHandler` (0x8001942) sets `MIDITimeToProcessBuffer` via macro [MIDI_TIMER_INTERRUPT](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/stm32-codec-midi-mmdsp-test-ST-Workbench/inc/midi_lowlevel.h#L18C9-L21).

### Length Handling
- Configured via MMIO register/descriptor field `DMA_BufferSize` in `USART2_Enable_Rx` (0x80017a6) to constant `MIDI_BUF_SIZE`: [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/stm32-codec-midi-mmdsp-test-ST-Workbench/src/midi_lowlevel.c#L54C37-L54C50)
- Actual size exchanged via MMIO register `NDTR`. Set during configuration in `DMA_Init` (see above)
- Check: `MIDI_process_buffer` does directly check the size, but keeps it in bounds via modulo `MIDIlastIndex`: [src](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/stm32-codec-midi-mmdsp-test-ST-Workbench/src/midi_lowlevel.c#L110C9-L110C22)




# Target: Modbus

DMA Summary: Shared RX/TX Buffer, Sync via Semaphore

Sources
- https://github.com/RiS3-Lab/DICE-DMA-Emulation/tree/master/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Modbus-ST-Workbench
- Source linked in paper: https://github.com/DoHelloWorld/stm32f3_Modbus_Slave_UART-DMA-FreeRTOS

Known DICE firmware patches: Remove CRC16, ...

## Milestones
Successful Processing: 0800231a (`modbusSlaveCheckID` success case in `modbusSlaveHandler`): [source](https://github.com/DoHelloWorld/stm32f3_Modbus_Slave_UART-DMA-FreeRTOS/blob/caaa26529927679dd3a074f0271d9bc276981c47/src/modbus_rtu.c#L70)

## Manual Configuration

- Location: 0x200041a8 (`modbusRxTxBuffer`)
- MMIO address: 0x40020064 (`DMA1_Channel5->CMAR`)
- Size: 256

## Transfer Mechanism Details
### Thread / Task
**Config**: modbusSlaveHardwareInit (0x080024c2): [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Modbus-ST-Workbench/src/modbus_rtu.c#L139C37-L139C53)

**Task / Loop**: modbusSlaveHandler (0x080022ec)
- **HW Activation**: modbusSlaveStartReceiving called from modbusSlaveHandler / IRQ handlers (08002304, 0800256c)
- **Sync Mechanism**: semaphore -> xSemaphoreTake (0x080022f6 as `xQueueGenericReceive`) on `xFrameReadySemaphore`
- **Processing**: `modbusSlaveCheckID`, `modbusSlaveParseFrame`

### Interrupt Handlers

- **IRQ Handlers**: DMA1_Channel5_IRQHandler (irq 31) / USART1_IRQHandler (irq 53): [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Modbus-ST-Workbench/src/modbus_rtu.c#L167-L188)
- **Sync Mechanism**: xSemaphoreGiveFromISR (0x80025b4 as `xQueueGiveFromISR`) on `xFrameReadySemaphore`

### Length Handling
- Configured via MMIO register `CNDTR` in `modbusSlaveStartReceiving`: [source](https://github.com/DoHelloWorld/stm32f3_Modbus_Slave_UART-DMA-FreeRTOS/blob/master/src/modbus_rtu.c#L179C21-L179C26)
- Actual size exchanged via global `modbusRxCount`. Set in IRQs (0x0800260c, 0x080025aa), via constant or with MMIO reg
- Check: modbusSlaveCheckFrameSize checks `len>5`: [src](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Modbus-ST-Workbench/src/modbus_rtu.c#L205C24-L205C45)


# Target: Soldering Station
- DMA Summary: RX-only, static buffer, with interrupts setting global flag  
- Sources: https://github.com/RiS3-Lab/DICE-DMA-Emulation/tree/master/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench  
- Sources linked in paper: https://github.com/PTDreamer/stm32_soldering_iron_controller  
- Known DICE firmware patches:  
	- HAL delay function does nothing: [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal.c#L325C1-L333C2)  
	- HAL dma error callback call patched out: [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_dma.c#L545C1-L549C8)  
	- watchdog patched out: [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/main.c#L104)  
	- timing changes: [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/main.c#L162)  
	- Clockconfig error handler removed: [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/main.c#L282-L285)  
	- Persistent settings change removed: [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/settings.c#L13)  
## Milestones  
- Finishing complete callback: `0x080082ec` [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/main.c#L156) (its a pretty bad one as it accesses the data, but no check is performed)  
- Tip temperature reached target temperature: `0x08007c56` [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/iron.c#L216)  
## Manual Configuration  
- Location: `0x20000904` (`adc_measures`)  
- MMIO address: DMA1 Channel 1 0x40020014 (`DMA_CHANNEL_5->CMAR`) (written at pc `0x08001664`)  
- Size: `sizeof(adc_measures)/sizeof(uint32_t)` = 20  
	- this is probably broken, as `adc_measures` is a bigger struct  
			  ```
				  				  typedef struct {
				  				  	uint16_t iron;
				  				  	uint16_t supply;
				  				  	uint16_t cold_junction;
				  				  	uint16_t reference;
				  				  } adc_measures_t;
				  				  volatile adc_measures_t adc_measures[10];
				  ```
	- checking the binary, we see that (,as is intuitive,) uint16_t is 2 bytes  
	- as `adc_measures` is length 10, the number checks out: `(10*8)/4 = 20`  
## Transfer Mechanism Details  
### Thread / Task  
- Config:   
    - `main` (`0x080081f2`, [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/main.c#L114))->`HAL_ADCEx_MultiModeStart_DMA`(`0x080014b0`, [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_adc_ex.c#L774))  
    - ->`HAL_DMA_Start_IT` (`0x080016ea`, [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_dma.c#L359))  
    - ->`DMA_SetConfig` (`0x08001664`, [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_dma.c#L693))  		  
- Task / Loop: `<function>` (0xADDR)  
	- HW Activation: `DMA_SetConfig` called from `HAL_DMA_Start_IT` (same call as config, so see above, pc `0x0800170c`)  
	- Sync Mechanism: global enum flag `iron_temp_measure_state`.  
		- Transitions:  
			- Init in main to `iron_temp_measure_idle`  
			- `iron_temp_measure_idle` -> `iron_temp_measure_requested` (in timer callback, [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/main.c#L190), pc `0x08007de0`)  
			- `iron_temp_measure_requested` -> `iron_temp_measure_pwm_stopped` (adc half complete callback, [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/main.c#L198), pc `0x08007e0c`)  
			- `iron_temp_measure_pwm_stopped` -> `iron_temp_measure_started` ( adc complete callback, [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/main.c#L213C29-L213C54), pc `0x08007e58`)  
			- `iron_temp_measure_started` -> `iron_temp_measure_ready` (adc complete callback, [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/main.c#L239C29-L239C52), pc `0x08007efa`)  
				- during this transition is where the dma accesses happen, usage is later  
				- this fills the `adc_values` and the derived value  
			- `iron_temp_measure_ready` -> `iron_temp_measure_idle` main [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/main.c#L171)  
	- Processing:  
		- `HAL_ADC_ConvCpltCallback` [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/main.c#L216-L239)  
			- creates the derived value `iron_temp_adc_avg`  
		- `readColdJunctionSensorTemp_mC` [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Drivers/generalIO/tempsensors.c#L26-L46)  
			- only used by gui to display values  
		- `iron_temp_adc_avg` derived value processing  
			- handleIron [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/iron.c#L215)  
  
### Interrupt Handlers  
- IRQ Handlers: `HAL_DMA_IRQHandler` (`DMA1_Channel1` 27 )  
- Sync Mechanism: see above  
### Length Handling  
- Configured via MMIO register `CNDTR` in function `DMA_SetConfig` (See complete chain and source above in config)  
- Size: `sizeof(adc_measures)/sizeof(uint32_t)` = 20  
- Check:  
	- array access and interpreted as struct  
	- always const index of 0 except for once ([here](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/main.c#L216C7-L216C69))  
	- the length check at the vairable index computes the size correctly: `sizeof(adc_measures)/sizeof(adc_measures[0])`  
	- but the length of the array is the wrong value anyway to configure the DMA size, we want `sizeof(adc_measures)` as according to the reference (about the `CNDTR` register): `Once the channel is enabled, this register is read-only, indicating the remaining bytes to be transmitted`  
	- so the computation can read up to 60 uninitialized values  
		- if they are 0, this can get problematic I guess?  
		- in any case it does not crash, so not interesting for the fuzzer  
		- [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Soldering-Station-ST-Workbench/Src/main.c#L114)  
# Target: Stepper motor  
- DMA Summary: RX/TX with different buffers (tx omitted because it is irrelevant for fuzzing), static buffers, timer interrupt-based polling  
- Sources: https://github.com/RiS3-Lab/DICE-DMA-Emulation/tree/master/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench  
- Sources linked in paper: https://github.com/omuzychko/StepperHub  
- Known DICE firmware patches:  
	- `TX_BUFFER_SIZE` / `RX_BUFFER_SIZE` size reduction from 4096 to 1024  
	- `if (__HAL_TIM_GET_FLAG(&htim14, TIM_FLAG_UPDATE))` patched out for `TIM8_TRG_COM_TIM14_IRQHandler`
- MMIO-based fallbacks: `HAL_UART_IRQHandler` will perform an MMIO-based fallback transfer via `UART_Receive_IT` in case of an error. Writes then occur to the receive buffer directly via the MMIO-based fallback.

## Milestones  
- this is a byte-by-byte stateful parser  
	- assume all commands are sent in the same dma request  
	- no partial transmission possible  
	- but multiple commands per dma sending are possible  
- Successful Processing:  
	- `0x08006786` (first field parsed of command): [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/src/stepperCommands.c#L592)  
	- `0x08006484` (cmd decoded, advance parser state to stepper): [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/src/stepperCommands.c#L437)  
	- `0x080064ec` (stepper decoded, advance parser state to param): [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/src/stepperCommands.c#L458)  
	- the param parser has two ways to set the state to value, so we set the value parser function as milestone instead  
		- `0x0800664c`: [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/src/stepperCommands.c#L531)  
## Manual Configuration  
- Location: `0x20000e28` (`rxBuffer`)  
- MMIO address: `0x40026094` (`DMA1_Stream5`, written at pc `0x0800207a`)  
- Size: 1024

## Transfer Mechanism Details  
### Thread / Task  
- Config:  
	- `main` -> `Serial_InitRxSequence` ([Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/src/main.c#L145))  
	- -> `HAL_UART_Receive_DMA` ([Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/src/serial.c#L185))  
	- -> `HAL_DMA_Start_IT`([Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/HAL_Driver/Src/stm32f4xx_hal_uart.c#L1379))  
	- -> `DMA_SetConfig` ([Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/HAL_Driver/Src/stm32f4xx_hal_dma.c#L474))  
- Task / Loop: regular poll with timer interrupt  
	- HW Activation: `SET_BIT` for config register in `HAL_UART_Receive_DMA` (`0x0800494a`)  
	- Sync Mechanism:  
		- none  
			- the firmware tries to constantly process the current index in the buffer  
			- `TIM8_TRG_COM_TIM14_IRQHandler` [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/src/main.c#L506-L521) -> `Serial_CheckRxTimeout` ([Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/src/serial.c#L192-L208))  
			- -> `Serial_RxCallback` ([Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/src/stepperCommands.c#L610-L612))  
			- -> `Decode` decoding data from here...  
		- I guess the best refresh trigger point is the timer interrupt: `0x08005b02`  
	- Processing: `Decode` [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/src/stepperCommands.c#L586)  
### Interrupt Handlers  
- IRQ Handlers:  
	- `DMA1_Stream5_IRQHandler` (irq 32) for data reception [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/src/stm32f4xx_it.c#L175)  
	- `TIM8_TRG_COM_TIM14_IRQHandler` (irq 61):  [Source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/src/main.c#L506)  
- Sync Mechanism: none  
### Length Handling  
- Configured via MMIO register `NDTR` in `DMA_SetConfig` (for full config chain see above): [source](https://github.com/RiS3-Lab/DICE-DMA-Emulation/blob/2b3b8c8b722abdbd7ff9e35fc7b02914fddf75df/DICE-Evaluation/ARM/Fuzzing/Firmware/Sources/Stepper-Motor-ST-Workbench/HAL_Driver/Src/stm32f4xx_hal_dma.c#L1157)  
- constant global buffer size of 1024 (4096 in original)  
