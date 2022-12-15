/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"

DigitalOut led1(LED1);

BufferedSerial      usb_pc(USBTX, USBRX);

void usb_pc_ISR(void){
    char rec_data_pc;
    int rec_length = 0;
    if(usb_pc.readable()){
        rec_length = usb_pc.read(&rec_data_pc, 1);
        usb_pc.write(&rec_data_pc, 1);
        if(rec_data_pc == 'a')        led1 = !led1;
        rec_data_pc = 'b';
        usb_pc.write(&rec_data_pc, 1);
    }
}

int main()
{
    usb_pc.set_baud(115200);
    usb_pc.sigio(callback(usb_pc_ISR));
    while (true){}
}
