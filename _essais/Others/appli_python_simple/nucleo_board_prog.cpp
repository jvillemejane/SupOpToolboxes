/****************************************************************************/
/*  Interface d'acquisition - Nucleo / version simple                       */
/****************************************************************************/
/*  LEnsE / Julien VILLEMEJANE       /   Institut d'Optique Graduate School */
/****************************************************************************/
/*  Brochage                                                                */
/*      USBTX, USBRX - connection to the computer @ 115200bauds             */
/*      LED1/D13 - LED de test                                              */
/****************************************************************************/
/*  Test réalisé sur Nucléo-L476RG                                          */
/****************************************************************************/

#include "mbed.h"

// inputs and outputs configuration
DigitalOut  debug_led(LED1);
Serial      rs232(USBTX, USBRX);

// System functions
void ISR_get_data(void);

// Variables
char data_received = 0;

// Main function
int main() {
    rs232.baud(115200);
    rs232.attach(&ISR_get_data);
    while(1) {    }
}

void ISR_get_data(){
    data_received = rs232.getc();
    switch(data_received){
        case 'a':
            rs232.putc('o');
            debug_led = 1;
            break;
        case 'e':
            rs232.putc('b');
            debug_led = 0;
            break;
        default:
            rs232.putc('k');            
    }
}