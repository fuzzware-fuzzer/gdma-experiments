/***********************************************************************************************************************
 * File Name    : spi_ep.c
 * Description  : Contains data structures and functions used in spi_ep.c.
 **********************************************************************************************************************/
/***********************************************************************************************************************
 * DISCLAIMER
 * This software is supplied by Renesas Electronics Corporation and is only intended for use with Renesas products. No
 * other uses are authorized. This software is owned by Renesas Electronics Corporation and is protected under all
 * applicable laws, including copyright laws.
 * THIS SOFTWARE IS PROVIDED "AS IS" AND RENESAS MAKES NO WARRANTIES REGARDING
 * THIS SOFTWARE, WHETHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING BUT NOT LIMITED TO WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. ALL SUCH WARRANTIES ARE EXPRESSLY DISCLAIMED. TO THE MAXIMUM
 * EXTENT PERMITTED NOT PROHIBITED BY LAW, NEITHER RENESAS ELECTRONICS CORPORATION NOR ANY OF ITS AFFILIATED COMPANIES
 * SHALL BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES FOR ANY REASON RELATED TO THIS
 * SOFTWARE, EVEN IF RENESAS OR ITS AFFILIATES HAVE BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.
 * Renesas reserves the right, without notice, to make changes to this software and to discontinue the availability of
 * this software. By using this software, you agree to the additional terms and conditions found by accessing the
 * following link:
 * http://www.renesas.com/disclaimer
 *
 * Copyright (C) 2020 Renesas Electronics Corporation. All rights reserved.
 ***********************************************************************************************************************/

#include "common_utils.h"
#include "spi_ep.h"
#include "pw_check.h"

/*******************************************************************************************************************//**
 * @addtogroup spi_ep
 * @{
 **********************************************************************************************************************/

/*
 * private function declarations
 */
static void error_print(void);

/* Wait counter for wait operation monitoring */
static volatile uint32_t g_wait_count = MAX_COUNT;

/* Event flags for master and slave */
static volatile spi_event_t g_master_event_flag;    // Master Transfer Event completion flag

/* SPI module buffers for Master and Slave */
static uint32_t g_master_rx_buff[BUFF_LEN];   // Master Receive Buffer

EXPORT_DMA_BUFFER_ALIAS(g_master_rx_buff);

/*******************************************************************************************************************//**
 * @brief       This functions initializes SPI master and slave modules.
 * @param[IN]   None
 * @retval      FSP_SUCCESS                  Upon successful open of SPI module
 * @retval      Any Other Error code apart from FSP_SUCCES  Unsuccessful open
 **********************************************************************************************************************/
fsp_err_t spi_init(void)
{
    fsp_err_t err = FSP_SUCCESS;     // Error status

    /* Open/Initialize SPI Master module */
    err = R_SPI_Open (&g_spi_master_ctrl, &g_spi_master_cfg);
    /* handle error */
    if (FSP_SUCCESS != err)
    {
        /* SPI Master Failure message */
        APP_ERR_PRINT("** R_SPI_Open API for SPI Master failed ** \r\n");
        /* Close SPI master */
        if ( (FSP_SUCCESS != R_SPI_Close(&g_spi_master_ctrl)))
        {
            /* SPI Master Close Failure message */
            APP_ERR_PRINT("** R_SPI_Close API for SPI Master failed ** \r\n");
        }
    }
    return err;
}

/*******************************************************************************************************************//**
 * @brief This function demos both R_SPI_Write() and R_SPI_Read() individually.
 * @param[IN]   None
 * @retval      FSP_SUCCESS                  Upon successful SPI Write and SPI Read
 * @retval      Any Other Error code apart from FSP_SUCCES  Unsuccessful Write and Read
 **********************************************************************************************************************/
fsp_err_t spi_write_and_read(void)
{
    fsp_err_t err = FSP_SUCCESS;     // Error status
    uint32_t num_bytes = RESET_VALUE;  // Number of bytes read by SEGGER real-time-terminal

    /* Cleaning buffers */
    memset(&g_master_rx_buff[0], NULL_CHAR, BUFF_LEN);

    /* Patch */
    num_bytes = 8;

    /* RTT Reads user input data 1 byte at a time. SPI transfers the data 4 bytes at a time.
     * With the below logic, we will calculate how many length of data has to be transferred. */
    // if(num_bytes % BITS_TO_BYTES != RESET_VALUE)
    // {
    //     num_bytes = (num_bytes/BITS_TO_BYTES) + 1U;
    // }
    // else
    // {
    //     num_bytes = num_bytes/BITS_TO_BYTES;
    //     g_master_tx_buff[num_bytes] = RESET_VALUE;
    // }


    /* Master receive data from Slave */
    err = R_SPI_Read(&g_spi_master_ctrl, g_master_rx_buff, num_bytes, SPI_BIT_WIDTH_32_BITS);
    /* Error handle */
    if(FSP_SUCCESS != err)
    {
        APP_ERR_PRINT("\r\nMaster R_SPI_Read() failed");
        return err;
    }

    /* Wait until slave write and master read complete */
    while(SPI_EVENT_TRANSFER_COMPLETE != g_master_event_flag)
    {
        /* Time out operation if SPI operation fails to complete */
        g_wait_count--;
        if(MIN_COUNT >= g_wait_count)
        {
            err = FSP_ERR_TIMEOUT;
            APP_ERR_PRINT("\r\nSPI module blocked in Write/Read operation.\r\n");
            error_print();
            return err;
        }
        else if (SPI_EVENT_TRANSFER_ABORTED == g_master_event_flag)
        {
            err = FSP_ERR_TRANSFER_ABORTED;
            APP_ERR_PRINT("\r\nSPI module blocked in Write/Read operation.\r\n");
            error_print();
            return err;
        }
        else
        {
            /* Do nothing */
        }
    }
    g_wait_count = MAX_COUNT;

    g_master_event_flag = (spi_event_t) RESET_VALUE;  // Reseting master_event flag

    check_password((void *) g_master_rx_buff);
    return FSP_SUCCESS;
}

/*******************************************************************************************************************//**
 * @brief This function close both SPI Master and Slave modules.
 * @param[IN]   None
 * @retval      FSP_SUCCESS                  SPI module closed successfully
 * @retval      Any Other Error code apart from FSP_SUCCES  Unsuccessful close
 **********************************************************************************************************************/
fsp_err_t spi_exit_demo(void)
{
    fsp_err_t err = FSP_SUCCESS;     // Error status

    /* Closing SPI Master module */
    err = R_SPI_Close(&g_spi_master_ctrl);
    /* Error Handle */
    if(FSP_SUCCESS != err)
    {
        APP_ERR_PRINT("\r\nMaster R_SPI_Close() failed");
    }
    return err;
}

/*******************************************************************************************************************//**
 * @brief Master SPI callback function.
 * @param[in]  p_args
 * @retval     None
 **********************************************************************************************************************/
void spi_master_callback(spi_callback_args_t * p_args)
{
    if (SPI_EVENT_TRANSFER_COMPLETE == p_args->event)
    {
        g_master_event_flag = SPI_EVENT_TRANSFER_COMPLETE;
    }
    else
    {
        g_master_event_flag = SPI_EVENT_TRANSFER_ABORTED;
    }
}

/*******************************************************************************************************************//**
 * @brief Slave SPI callback function.
 * @param[in]  p_args
 * @retval     None
 **********************************************************************************************************************/
void spi_slave_callback(spi_callback_args_t * p_args)
{
    return;
}

/*******************************************************************************************************************//**
 * @brief This function prints the error message.
 * @param[IN]   None
 * @retval      None
 **********************************************************************************************************************/
static void error_print(void)
{
    APP_PRINT("\r\nError in configuration or connection.\r\n");
    APP_PRINT( "\r\nReset the MCU...\r\n");
}

/*******************************************************************************************************************//**
 * @brief This function closes all the opened SPI modules before the project ends up in an Error Trap.
 * @param[IN]   None
 * @retval      None
 **********************************************************************************************************************/
void spi_clean_up(void)
{
    fsp_err_t err = FSP_SUCCESS;

    /* Close SPI module */
    err = R_SPI_Close(&g_spi_master_ctrl);
    /* handle error */
    if (FSP_SUCCESS != err)
    {
        /* SPI Close failure message */
        APP_ERR_PRINT("** R_SPI_Close API for master failed **  \r\n");
    }
}

/*******************************************************************************************************************//**
 * @} (end addtogroup spi_ep)
 **********************************************************************************************************************/
