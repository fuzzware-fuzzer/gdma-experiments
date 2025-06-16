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
#include <stdint.h>
#include <string.h>
#include "uartdrv_app.h"
#include "sl_uartdrv_instances.h"
#include "sl_power_manager.h"
#include "pw_check.h"
#include "message.h"
#include "parser.h"
#include "serialiser.h"
#include "errors.h"
/*******************************************************************************
 *******************************   DEFINES   ***********************************
 ******************************************************************************/
#define INPUT_BUFSIZE    100

/*******************************************************************************
 ***************************  LOCAL VARIABLES   ********************************
 ******************************************************************************/
mqtt_parser_t parser;
mqtt_serialiser_t serialiser;
mqtt_message_t message;

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
  ssize_t nread = 0; 
  if (transferStatus == ECODE_EMDRV_UARTDRV_OK) {
    uint8_t mqtt_buf[INPUT_BUFSIZE] = {0};
    memcpy(mqtt_buf, dma_buf, INPUT_BUFSIZE);    
    // mqtt parser interaction
    int rc;
    do {
      // execute the parser with the dma buffer contents as its input
      rc = mqtt_parser_execute(&parser, &message, mqtt_buf, INPUT_BUFSIZE, &nread);
      if (rc == MQTT_PARSER_RC_WANT_MEMORY) {
	// Increase memory if need be
        mqtt_parser_buffer(&parser, malloc(parser.buffer_length), parser.buffer_length);  
      }
    } while (rc == MQTT_PARSER_RC_CONTINUE || rc == MQTT_PARSER_RC_WANT_MEMORY);

    // Serialize the parsed message
    size_t packet_length = mqtt_serialiser_size(&serialiser, &message);
    uint8_t* packet = malloc(packet_length);
    mqtt_serialiser_write(&serialiser, &message, packet, packet_length);

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
	
  // INIT MQTT
  mqtt_parser_init(&parser);
  mqtt_serialiser_init(&serialiser);
  mqtt_message_init(&message);

  // Require at least EM2 from Power Manager
  sl_power_manager_add_em_requirement(SL_POWER_MANAGER_EM2);

  // Non-blocking receive
  UARTDRV_Receive(sl_uartdrv_leuart_vcom_handle,
                  dma_buf, INPUT_BUFSIZE,
                  UART_rx_callback);
}

/***************************************************************************//**
 * Ticking function.
 ******************************************************************************/
void uartdrv_app_process_action(void)
{
}
