/*
 * @brief UART example
 * This example show how to use the UART in 3 modes : Polling, Interrupt and DMA
 *
 * @note
 * Copyright(C) NXP Semiconductors, 2013
 * All rights reserved.
 *
 * @par
 * Software that is described herein is for illustrative purposes only
 * which provides customers with programming information regarding the
 * LPC products.  This software is supplied "AS IS" without any warranties of
 * any kind, and NXP Semiconductors and its licensor disclaim any and
 * all warranties, express or implied, including all implied warranties of
 * merchantability, fitness for a particular purpose and non-infringement of
 * intellectual property rights.  NXP Semiconductors assumes no responsibility
 * or liability for the use of the software, conveys no license or rights under any
 * patent, copyright, mask work right, or any other intellectual property rights in
 * or to any products. NXP Semiconductors reserves the right to make changes
 * in the software without notification. NXP Semiconductors also makes no
 * representation or warranty that such application will be suitable for the
 * specified use without further testing or modification.
 *
 * @par
 * Permission to use, copy, modify, and distribute this software and its
 * documentation is hereby granted, under NXP Semiconductors' and its
 * licensor's relevant copyrights in the software, without fee, provided that it
 * is used in conjunction with NXP Semiconductors microcontrollers.  This
 * copyright, permission, and disclaimer notice must appear in all copies of
 * this code.
 */

#include "chip.h"
#include "board.h"
#include "isup.h"
#include "libss7.h"
#include "mtp2.h"

/*****************************************************************************
 * Private types/enumerations/variables
 ****************************************************************************/
#if (defined(BOARD_HITEX_EVA_1850) || defined(BOARD_HITEX_EVA_4350))
#define UARTNum 0

#elif (defined(BOARD_KEIL_MCB_1857) || defined(BOARD_KEIL_MCB_4357))
#define UARTNum 3

#elif (defined(BOARD_NGX_XPLORER_1830) || defined (BOARD_NGX_XPLORER_4330))
#define UARTNum 0

#elif defined(BOARD_NXP_LPCLINK2_4370)
#define UARTNum 2

#elif (defined(BOARD_NXP_LPCXPRESSO_4337) || defined(BOARD_NXP_LPCXPRESSO_1837))
#define UARTNum 0

#else
#error No UART selected for undefined board
#endif

#if (UARTNum == 0)
#define LPC_UART LPC_USART0
#define UARTx_IRQn  USART0_IRQn
#define UARTx_IRQHandler UART0_IRQHandler
#define _GPDMA_CONN_UART_Tx GPDMA_CONN_UART0_Tx
#define _GPDMA_CONN_UART_Rx GPDMA_CONN_UART0_Rx
#elif (UARTNum == 1)
#define LPC_UART LPC_UART1
#define UARTx_IRQn  UART1_IRQn
#define UARTx_IRQHandler UART1_IRQHandler
#define _GPDMA_CONN_UART_Tx GPDMA_CONN_UART1_Tx
#define _GPDMA_CONN_UART_Rx GPDMA_CONN_UART1_Rx
#elif (UARTNum == 2)
#define LPC_UART LPC_USART2
#define UARTx_IRQn  USART2_IRQn
#define UARTx_IRQHandler UART2_IRQHandler
#define _GPDMA_CONN_UART_Tx GPDMA_CONN_UART2_Tx
#define _GPDMA_CONN_UART_Rx GPDMA_CONN_UART2_Rx
#elif (UARTNum == 3)
#define LPC_UART LPC_USART3
#define UARTx_IRQn  USART3_IRQn
#define UARTx_IRQHandler UART3_IRQHandler
#define _GPDMA_CONN_UART_Tx GPDMA_CONN_UART3_Tx
#define _GPDMA_CONN_UART_Rx GPDMA_CONN_UART3_Rx
#endif

#define DMA_SIZE 	128

typedef struct {
        uint32_t src;       /**< Source Address */
        uint32_t dst;       /**< Destination address */
        uint32_t lli;       /**< Next LLI address, otherwise set to '0' */
        uint32_t ctrl;       /**< GPDMA Control of this LLI */
} GPDMA_LLI_Type;


uint8_t DMADest_Buffer[DMA_SIZE+8];
// 8 byte padding to have a separation between buffers
uint8_t DMADest_Buffer_2[DMA_SIZE];
/* Transmit and receive ring buffers */
STATIC RINGBUFF_T txring, rxring;


/* DMA variables and functions declaration */
static uint8_t dmaChannelNumTx, dmaChannelNumRx;

static volatile uint32_t channelTC;	/* Terminal Counter flag for Channel */
static volatile uint32_t channelTCErr;
static FunctionalState  isDMATx = ENABLE;

/*****************************************************************************
 * Public types/enumerations/variables
 ****************************************************************************/

/*****************************************************************************
 * Private functions
 ****************************************************************************/

/* Initialize DMA for UART, enable DMA controller and enable DMA interrupt */
static void App_DMA_Init(void)
{
	/* Initialize GPDMA controller */
	Chip_GPDMA_Init(LPC_GPDMA);
	/* Setting GPDMA interrupt */
	NVIC_DisableIRQ(DMA_IRQn);
	NVIC_SetPriority(DMA_IRQn, ((0x01 << 3) | 0x01));
	NVIC_EnableIRQ(DMA_IRQn);
}

/* DeInitialize DMA for UART, free transfer channels and disable DMA interrupt */
static void App_DMA_DeInit(void)
{
	Chip_GPDMA_Stop(LPC_GPDMA, dmaChannelNumTx);
	Chip_GPDMA_Stop(LPC_GPDMA, dmaChannelNumRx);
	NVIC_DisableIRQ(DMA_IRQn);
}

/* PATCHED DMA ROUTINE */
static void App_DMA_Test(void)
{
	DMA_TransferDescriptor_t DMA_LLI_Struct[2], templli;

	App_DMA_Init();

	int res = -1;

	//prep descriptors
	res = Chip_GPDMA_PrepareDescriptor(LPC_GPDMA, (uint32_t)&DMA_LLI_Struct[0], _GPDMA_CONN_UART_Rx, (uint32_t)DMADest_Buffer,
	    							DMA_SIZE, GPDMA_TRANSFERTYPE_P2M_CONTROLLER_DMA, (uint32_t)&DMA_LLI_Struct[1]);

	res = Chip_GPDMA_PrepareDescriptor(LPC_GPDMA, (uint32_t)&DMA_LLI_Struct[1], _GPDMA_CONN_UART_Rx, ((uint32_t)DMADest_Buffer_2),
	    							DMA_SIZE, GPDMA_TRANSFERTYPE_P2M_CONTROLLER_DMA, 0);


	// There seems to be an (ancient?) bug in the Scatter-gather API?
	// https://community.nxp.com/t5/LPC-Microcontrollers/GPDMA-DAC-V2-12/m-p/583777
	// We need to create an LLI with the peripheral value (in this case, src set
	// to the lookup value, not the pointer)

	// create a temporary LLI for the API call, this can be discarded after the call
	templli.ctrl=DMA_LLI_Struct[0].ctrl;
	templli.lli=(uint32_t)&DMA_LLI_Struct[1];
	templli.src=LPC_GPDMA;
	templli.dst=DMA_LLI_Struct[0].dst;

    // init ss7 parser
    struct ss7 *ss7;
    ss7 = ss7_new(SS7_ANSI);
    ss7_add_link(ss7, SS7_TRANSPORT_DAHDIDCHAN, 10, -1, 0);
    ss7->debug = SS7_DEBUG_MTP2 | SS7_DEBUG_MTP3 | SS7_DEBUG_ISUP;
    ss7->links[0]->state = MTP_INSERVICE;

    for (int i = 0; i < 10; i++) {
        // get a channel number and start the transfer
        dmaChannelNumRx = 0;
        isDMATx = DISABLE;
        channelTC = channelTCErr = 0;
        Chip_GPDMA_ChannelCmd(LPC_GPDMA, dmaChannelNumRx, DISABLE);
        res = Chip_GPDMA_SGTransfer(LPC_GPDMA, dmaChannelNumRx, (uint32_t)&templli, GPDMA_TRANSFERTYPE_P2M_CONTROLLER_DMA);
        if (res != 1){
            return;
        }
        while (!channelTC) {
                asm volatile("wfimark: .global wfimark":); // set marker for interrupt
                __WFI();
        }

        mtp2_receive(ss7->links[0], DMADest_Buffer, DMA_SIZE);
        mtp2_receive(ss7->links[0], DMADest_Buffer_2, DMA_SIZE);

    }

    ss7_destroy(ss7);
	App_DMA_DeInit();
}

/*****************************************************************************
 * Public functions
 ****************************************************************************/

/**
 * @brief	GPDMA interrupt handler sub-routine
 * @return	Nothing
 */
void DMA_IRQHandler(void)
{
	uint8_t dmaChannelNum;
	if (isDMATx) {
		dmaChannelNum = dmaChannelNumTx;
	}
	else {
		dmaChannelNum = dmaChannelNumRx;
	}
	if (Chip_GPDMA_Interrupt(LPC_GPDMA, dmaChannelNum) == SUCCESS) {
		channelTC++;
	}
	else {
		channelTCErr++;
	}
}

/**
 * @brief	UART interrupt handler sub-routine
 * @return	Nothing
 */
void UARTx_IRQHandler(void)
{
	Chip_UART_IRQRBHandler(LPC_UART, &rxring, &txring);
}

/**
 * @brief	Main UART program body
 * @return	Always returns -1
 */
int main(void)
{
	int ret = 0;

	SystemCoreClockUpdate();
	Board_Init();
	Board_UART_Init(LPC_UART);

	Chip_UART_Init(LPC_UART);
	Chip_UART_SetBaud(LPC_UART, 115200);
	Chip_UART_ConfigData(LPC_UART, UART_LCR_WLEN8 | UART_LCR_SBS_1BIT); /* Default 8-N-1 */

	/* Enable UART Transmit */
	Chip_UART_TXEnable(LPC_UART);

	/* Reset FIFOs, Enable FIFOs and DMA mode in UART */
	Chip_UART_SetupFIFOS(LPC_UART, (UART_FCR_FIFO_EN | UART_FCR_RX_RS |
							UART_FCR_TX_RS | UART_FCR_DMAMODE_SEL | UART_FCR_TRG_LEV0));

    App_DMA_Test();

	/* DeInitialize UART0 peripheral */
	Chip_UART_DeInit(LPC_UART);

    asm volatile("exit_main: .global exit_main":); // set marker for end of execution
	return ret;
}
