/****************************************************************************
 * @file     main.c
 * @version  V3.00
 * $Revision: 3 $
 * $Date: 15/07/02 11:18a $
 * @brief
 *           Transmit and receive UART data with PDMA.
 *
 * @note
 * Copyright (C) 2014~2015 Nuvoton Technology Corp. All rights reserved.
 *
 ******************************************************************************/
#include <stdio.h>
#include "NUC123.h"
#include <pw_check.h>

#define HCLK_CLOCK  72000000

#define UART_RX_DMA_CH 0
#define UART_TX_DMA_CH 1


/*---------------------------------------------------------------------------------------------------------*/
/* Global variables                                                                                        */
/*---------------------------------------------------------------------------------------------------------*/
int32_t UART_TEST_LENGTH = 8;
uint8_t SrcArray[8];
uint8_t DestArray[8];
volatile int32_t IntCnt;
volatile int32_t IsTestOver;
volatile uint32_t g_u32TwoChannelPdmaTest=0;
extern char GetChar(void);

EXPORT_DMA_BUFFER_ALIAS (DestArray)

/*---------------------------------------------------------------------------------------------------------*/
/* Define functions prototype                                                                              */
/*---------------------------------------------------------------------------------------------------------*/
int main(void);


/*---------------------------------------------------------------------------------------------------------*/
/* Clear buffer funcion                                                                              	   */
/*---------------------------------------------------------------------------------------------------------*/
void ClearBuf(uint32_t u32Addr, uint32_t u32Length, uint8_t u8Pattern)
{
	uint8_t* pu8Ptr;
	uint32_t i;
	
	pu8Ptr = (uint8_t *)u32Addr;
	
	for (i=0; i<u32Length; i++)
	{
		*pu8Ptr++ = u8Pattern;
	}
}

/*---------------------------------------------------------------------------------------------------------*/
/* Bulid Src Pattern function                                                                         	   */
/*---------------------------------------------------------------------------------------------------------*/
void BuildSrcPattern(uint32_t u32Addr, uint32_t u32Length)
{
    uint32_t i=0,j,loop;
    uint8_t* pAddr;
    
    pAddr = (uint8_t *)u32Addr;
    
    do {
        if (u32Length > 256)
	    	loop = 256;
	    else
	    	loop = u32Length;
	    	
	   	u32Length = u32Length - loop;    	

        for(j=0;j<loop;j++)
            *pAddr++ = (uint8_t)(j+i);
            
	    i++;        
	} while ((loop !=0) || (u32Length !=0));         
}

/*---------------------------------------------------------------------------------------------------------*/
/* UART Tx PDMA Channel Configuration                                                                      */
/*---------------------------------------------------------------------------------------------------------*/
void PDMA_UART_TxTest(void)
{
    /* UART Tx PDMA channel configuration */
    /* Set transfer width (8 bits) and transfer count */
    PDMA_SetTransferCnt(UART_TX_DMA_CH, PDMA_WIDTH_8, UART_TEST_LENGTH);

    /* Set source/destination address and attributes */
    PDMA_SetTransferAddr(UART_TX_DMA_CH, (uint32_t)SrcArray, PDMA_SAR_INC, (uint32_t)&UART1->THR, PDMA_DAR_FIX);

    /* Set service selection; set Memory-to-Peripheral mode. */
    PDMA_SetTransferMode(UART_TX_DMA_CH, PDMA_UART1_TX, FALSE, 0);
}

/*---------------------------------------------------------------------------------------------------------*/
/* UART Rx PDMA Channel Configuration                                                                      */
/*---------------------------------------------------------------------------------------------------------*/
void PDMA_UART_RxTest(void)
{
	// if this really sets up peripheral to memory, then we are good here
	// however, this eclipse ide cannot find some of the constants and as such I dont really know the values of constants

    /* UART Rx PDMA channel configuration */        
    /* Set transfer width (8 bits) and transfer count */
    PDMA_SetTransferCnt(UART_RX_DMA_CH, PDMA_WIDTH_8, UART_TEST_LENGTH);
    
    /* Set source/destination address and attributes */
    // educated guess: set source to uart0-> rbr (the data reg), source addr fixed
    // destination address is dest array, incrementing
    PDMA_SetTransferAddr(UART_RX_DMA_CH, (uint32_t)&UART0->RBR, PDMA_SAR_FIX, (uint32_t)DestArray, PDMA_DAR_INC);

    /* Set service selection; set Peripheral-to-Memory mode. */
    PDMA_SetTransferMode(UART_RX_DMA_CH, PDMA_UART0_RX, FALSE, 0);
}

/*---------------------------------------------------------------------------------------------------------*/
/* PDMA Callback function                                                                           	   */
/*---------------------------------------------------------------------------------------------------------*/

void PDMA_Callback(void)
{
 	int32_t i ;
 	// here we can do the password checking and printing
 	printf("\tTransfer Done %d!\t",++IntCnt);

    /* Show UART Rx data */
	for(i=0;i<UART_TEST_LENGTH;i++)
        printf(" 0x%x(%c),",inpb(((uint32_t)DestArray+i)),inpb(((uint32_t)DestArray+i)));
	printf("\n");
	check_password(DestArray);

}

void PDMA_IRQHandler(void)
{    
    /* Get PDMA Block transfer down interrupt status */
    if(PDMA_GET_CH_INT_STS(UART_RX_DMA_CH) & PDMA_ISR_BLKD_IF_Msk)
    {
        /* Clear PDMA Block transfer down interrupt flag */   
        PDMA_CLR_CH_INT_FLAG(UART_RX_DMA_CH, PDMA_ISR_BLKD_IF_Msk);   
        
        /* Handle PDMA block transfer done interrupt event */
		PDMA_Callback();
    }      
}


/*---------------------------------------------------------------------------------------------------------*/
/* PDMA Sample Code:                                                                                  	   */
/*         i32option : ['1'] UART1 TX/RX PDMA Loopback                                                     */
/*                     [Others] UART1 RX PDMA test                                                         */
/*---------------------------------------------------------------------------------------------------------*/
void PDMA_UART()
{    
    /* Source data initiation */    
	BuildSrcPattern((uint32_t)SrcArray, UART_TEST_LENGTH);
    ClearBuf((uint32_t)DestArray, UART_TEST_LENGTH, 0xFF);
    
    /* Reset PDMA module */
    SYS_ResetModule(PDMA_RST);

	UART_TEST_LENGTH = 8;	   /* Test Length */

    /* Enable PDMA channel clock */  
    PDMA_Open( (1 << UART_RX_DMA_CH) );   

    /* UART Rx PDMA configuration */          
    PDMA_UART_RxTest();  

	/* Enable PDMA Block Transfer Done Interrupt */ 
    PDMA_EnableInt(UART_RX_DMA_CH, PDMA_IER_BLKD_IE_Msk);    
 	IntCnt = 0;       
    IsTestOver = FALSE;        
    NVIC_EnableIRQ(PDMA_IRQn);
    
    /* Enable UART0 RDA interrupt */

	UART_EnableInt(UART0, UART_IER_RDA_IEN_Msk);
	/* Trigger PDMA */	
    PDMA_Trigger(UART_RX_DMA_CH);
    
    // disable transmit interrupt
    UART0->IER &= ~UART_IER_DMA_TX_EN_Msk;
    // enable receive interrupt
    UART0->IER |= UART_IER_DMA_RX_EN_Msk;

    /* Wait for PDMA operation finish */
    while(IsTestOver == FALSE);   

    /* Disable UART Tx and Rx PDMA function */    
	UART0->IER &= ~(UART_IER_DMA_TX_EN_Msk|UART_IER_DMA_RX_EN_Msk);
    
    /* Disable PDMA channel */
    PDMA_Close();    
    
	/* Disable PDMA Interrupt */
    PDMA_DisableInt(UART_RX_DMA_CH, PDMA_IER_BLKD_IE_Msk);  
    NVIC_DisableIRQ(PDMA_IRQn);    
    
    /* Disable UART0 RDA interrupt */
    UART_DisableInt(UART0, UART_IER_RDA_IEN_Msk);   	
}

void SYS_Init(void)
{
    /*---------------------------------------------------------------------------------------------------------*/
    /* Init System Clock                                                                                       */
    /*---------------------------------------------------------------------------------------------------------*/

    /* Enable XT1_OUT(PF0) and XT1_IN(PF1) */
    SYS->GPF_MFP &= ~(SYS_GPF_MFP_PF0_Msk | SYS_GPF_MFP_PF1_Msk);
    SYS->GPF_MFP |= SYS_GPF_MFP_PF0_XT1_OUT | SYS_GPF_MFP_PF1_XT1_IN;

    /* Enable Internal RC 22.1184MHz clock */
    CLK_EnableXtalRC(CLK_PWRCON_OSC22M_EN_Msk);

    /* Waiting for Internal RC clock ready */
    CLK_WaitClockReady(CLK_CLKSTATUS_OSC22M_STB_Msk);

    /* Switch HCLK clock source to Internal RC and HCLK source divide 1 */
    CLK_SetHCLK(CLK_CLKSEL0_HCLK_S_HIRC, CLK_CLKDIV_HCLK(1));

    /* Enable external XTAL 12MHz clock */
    CLK_EnableXtalRC(CLK_PWRCON_XTL12M_EN_Msk);

    /* Waiting for external XTAL clock ready */
    CLK_WaitClockReady(CLK_CLKSTATUS_XTL12M_STB_Msk);

    /* Set core clock as HCLK_CLOCK */
    CLK_SetCoreClock(HCLK_CLOCK);

    /* Enable UART module clock */
    CLK_EnableModuleClock(UART0_MODULE);
    CLK_EnableModuleClock(UART1_MODULE);    
    
    /* Enable PDMA clock source */
    CLK_EnableModuleClock(PDMA_MODULE);    

    /* Select UART module clock source as HXT and UART module clock divider as 1 */
    CLK_SetModuleClock(UART0_MODULE, CLK_CLKSEL1_UART_S_HXT, CLK_CLKDIV_UART(1));
    CLK_SetModuleClock(UART1_MODULE, CLK_CLKSEL1_UART_S_HXT, CLK_CLKDIV_UART(1)); 

    /*---------------------------------------------------------------------------------------------------------*/
    /* Init I/O Multi-function                                                                                 */
    /*---------------------------------------------------------------------------------------------------------*/

    /* Set GPB multi-function pins for UART0 RXD(PB.0) and TXD(PB.1) */
    /* Set GPB multi-function pins for UART1 RXD(PB.4) and TXD(PB.5) */

    SYS->GPB_MFP &= ~(SYS_GPB_MFP_PB0_Msk | SYS_GPB_MFP_PB1_Msk | SYS_GPB_MFP_PB4_Msk | SYS_GPB_MFP_PB5_Msk);
    SYS->GPB_MFP |= (SYS_GPB_MFP_PB0_UART0_RXD | SYS_GPB_MFP_PB1_UART0_TXD | SYS_GPB_MFP_PB4_UART1_RXD | SYS_GPB_MFP_PB5_UART1_TXD);

    SYS->ALT_MFP &= ~(SYS_ALT_MFP_PB4_Msk | SYS_ALT_MFP_PB5_Msk);
    SYS->ALT_MFP |= (SYS_ALT_MFP_PB4_UART1_RXD | SYS_ALT_MFP_PB5_UART1_TXD);

}

void UART0_Init()
{
    /*---------------------------------------------------------------------------------------------------------*/
    /* Init UART                                                                                               */
    /*---------------------------------------------------------------------------------------------------------*/
    /* Reset UART0 */
    SYS_ResetModule(UART0_RST);

    /* Configure UART0 and set UART0 Baudrate */
    UART_Open(UART0, 115200);
}


/*---------------------------------------------------------------------------------------------------------*/
/* MAIN function                                                                                           */
/*---------------------------------------------------------------------------------------------------------*/

int main(void)
{
   	uint8_t unItem;       
    
    /* Unlock protected registers */
    SYS_UnlockReg();

    /* Init System, peripheral clock and multi-function I/O */
    SYS_Init();

    /* Lock protected registers */
    SYS_LockReg();

    /* Init UART0 for printf and testing */
    UART0_Init();

    /*---------------------------------------------------------------------------------------------------------*/
    /* SAMPLE CODE                                                                                             */
    /*---------------------------------------------------------------------------------------------------------*/

    printf("\n\nCPU @ %d Hz\n", SystemCoreClock);

    printf("\nUART PDMA Sample Program");

    /* UART PDMA sample function */
	do
	{	// 2 is loopback test
		PDMA_UART();
    }while(1);

    while(1);
}

