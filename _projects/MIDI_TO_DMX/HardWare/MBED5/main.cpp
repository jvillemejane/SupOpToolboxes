/****************************************************************************/
/*  Test DMX512 + MOD-24LR / nrf24L01                                       */
/****************************************************************************/
/*  LEnsE / Julien VILLEMEJANE       /   Institut d'Optique Graduate School */
/****************************************************************************/
/*  Brochage                                                                */
/*      TO COMPLETE                                                         */
/****************************************************************************/
/*  Test réalisé sur Nucléo-L476RG                                          */
/****************************************************************************/

#include    "mbed.h"
#include    "DMX_MIDI.h"

Serial          debug_pc(USBTX, USBRX);
DigitalOut      debug_out(D13);

// Main
int main() {
    debug_pc.baud(115200);
    debug_pc.printf("Test\r\n");
    
    // Initialisation périphériques
    initDMX();
    initMIDI();
    
    dmx_data[0] = 0;
    dmx_data[3] = 255;
    dmx_data[4] = 255;
    dmx_data[5] = 100;
    dmx_data[6] = 50;

    while(1) { 
        /* MIDI */
        
        if(isNoteMIDIdetected()){
            if(note_data == 0x3C){
                dmx_data[4] = 2*velocity_data;
                dmx_data[5] = 0;
                dmx_data[6] = 0;
            }
            if(note_data == 0x3E){
                dmx_data[4] = 0;
                dmx_data[5] = velocity_data;
                dmx_data[6] = 0;
            }                
            resetNoteMIDI();
        }
        
        if(isCCMIDIdetected()){
            if(control_ch == 1){
                dmx_data[4] = 2 * control_value;
                dmx_data[12] = 2 * control_value;
            }
            resetCCMIDI();
        }
        
        updateDMX();
        wait_us(10000);
        
    }
}
