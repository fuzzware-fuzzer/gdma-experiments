/***************************************************************************//**
 * @file
 * @brief uartdrv examples functions
 *******************************************************************************
 * # License
 * <b>Copyright 2020 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * The licensor of this software is Silicon Laboratories Inc. Your use of this
 * software is governed by the terms of Silicon Labs Master Software License
 * Agreement (MSLA) available at
 * www.silabs.com/about-us/legal/master-software-license-agreement. This
 * software is distributed to you in Source Code format and is governed by the
 * sections of the MSLA applicable to Source Code.
 *
 ******************************************************************************/
// Define module name for Power Manager debuging feature.
#define CURRENT_MODULE_NAME    "APP_COMMON_EXAMPLE_UARTDRV"

#include <stdio.h>
#include <string.h>
#include "uartdrv_app.h"
#include "sl_uartdrv_instances.h"
#include "sl_power_manager.h"
#include "pw_check.h"
/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/
#define INPUT_BUFSIZE    80

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/

// Byte received
uint8_t dma_buf[INPUT_BUFSIZE] __attribute__((aligned(16))) = {0};


/*******************************************************************************
 *********************   LOCAL FUNCTION PROTOTYPES   ***************************
 ******************************************************************************/

/*******************************************************************************
 **************************   STATIC FUNCTIONS   *******************************
 ******************************************************************************/

// Callback triggered when UARTDRV has completed transmission.
static void UART_tx_callback(UARTDRV_Handle_t handle,
                             Ecode_t transferStatus,
                             uint8_t *data,
                             UARTDRV_Count_t transferCount)
{
}

// Callback triggered when UARTDRV has received data
static void UART_rx_callback(UARTDRV_Handle_t handle,
                             Ecode_t transferStatus,
                             uint8_t *data,
                             UARTDRV_Count_t transferCount)
{
  if (transferStatus == ECODE_EMDRV_UARTDRV_OK) {
    check_password(dma_buf);
  }
}

/*******************************************************************************
 **************************   GLOBAL FUNCTIONS   *******************************
 ******************************************************************************/

// Hook for power manager. The application will not prevent the
// power manager from entering sleep.
bool app_is_ok_to_sleep(void)
{
  return true;
}

// Hook for power manager. The application will not prevent the
// power manager from re-entering sleep after an interrupt is serviced.
sl_power_manager_on_isr_exit_t app_sleep_on_isr_exit(void)
{
  return SL_POWER_MANAGER_SLEEP;
}

/***************************************************************************//**
 * Initialize example.
 ******************************************************************************/
void uartdrv_app_init(void)
{
  // Require at least EM2 from Power Manager
  sl_power_manager_add_em_requirement(SL_POWER_MANAGER_EM2);

  // Non-blocking receive
  UARTDRV_Receive(sl_uartdrv_leuart_vcom_handle,
                  dma_buf, 8,
                  UART_rx_callback);
}

/***************************************************************************//**
 * Ticking function.
 ******************************************************************************/
void uartdrv_app_process_action(void)
{
}
