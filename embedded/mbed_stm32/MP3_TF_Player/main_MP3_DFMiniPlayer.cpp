/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"
#include "MP3_DFMiniPlayer.h"

#define WAIT_TIME_MS 500 
DigitalOut      led1(LED1);
InterruptIn     playpauseBtn(BUTTON1);
bool            playorpause;

UnbufferedSerial	my_pc(USBTX, USBRX);
char		chStr[128];

UnbufferedSerial	my_serial(A4, A5);
MP3_DFMiniPlayer	my_player(&my_serial);

void ISR_playpause(void){
    playorpause = !playorpause;
    if(playorpause){
        my_player.playCmd();
    }
    else{
        my_player.pauseCmd();
    }
}

//////////// MAIN
int main()
{
	my_pc.baud(115200);
    my_player.setDebugSerial(&my_pc);

    playpauseBtn.fall(&ISR_playpause);
	
	sprintf(chStr, "Mbed OS %d.%d.%d.\n", MBED_MAJOR_VERSION, MBED_MINOR_VERSION, MBED_PATCH_VERSION);
	my_pc.write(chStr, strlen(chStr));

    my_player.reset();
	
	// Wait until MP3 Player is ready
    while(my_player.waitAvailable() < 0){
        int k = my_player.getDataCnt();
        sprintf(chStr, "Player NOT READY. %d \n", k);
        my_pc.write(chStr, strlen(chStr));
        thread_sleep_for(500);        
    }	

	sprintf(chStr, "Player OK.\n");
	my_pc.write(chStr, strlen(chStr));

    
    my_player.playTrack(2, 1);

    while (true)
    {
        led1 = !led1;


        thread_sleep_for(WAIT_TIME_MS);
    }
}
