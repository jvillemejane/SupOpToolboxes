/**
 * FILENAME :        COLOR_14_CLICK.cpp          
 *
 * DESCRIPTION :
 *       COLOR_14_CLICK / RGB Sensor from MikroE.
 *
 *       This module allows to measure Red Green and Blue light intensity (and IR)
 *  with a specific I2C device - APDS-9151 from BroadCom
 *       More informations : https://www.broadcom.com/products/optical-sensors/integrated-ambient-light-and-proximity-sensors/apds-9151
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    07/feb/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */


 #include <mbed.h>
 #include "COLOR_14_CLICK.h"

Color_14_Click::Color_14_Click(I2C *_i2c, InterruptIn *_int){
    /* Initialisation of interrupt input */
    if (_int){ delete __int; }
    __int=_int;
    /* Initialisation of i2c module */
    if (_i2c){ delete __i2c; }
    __i2c=_i2c;
    __i2c->frequency(400000);   // Frequency of 400kHz
    thread_sleep_for(10);      // 10 ms
}

void Color_14_Click::powerUp(void){
    cmd[0] = COLOR_14_CLICK_MAIN_CTRL;
    cmd[1] = 0b00000100;
    ack1 = __i2c->write(COLOR_14_CLICK_ADD << 1, cmd, 2);
    if(DEBUG_MODE) printf("Init Acq = %d\r\n", ack1);
    wait_us(1000);
}

void Color_14_Click::initRGBSensor(void){
    cmd[0] = COLOR_14_CLICK_MAIN_CTRL;
    cmd[1] = 0b00000110;
    ack1 = __i2c->write(COLOR_14_CLICK_ADD << 1, cmd, 2);
    if(DEBUG_MODE) printf("Init Acq = %d\r\n", ack1);
    wait_us(1000);
}

int Color_14_Click::getPartID(void){
    // Part ID Status
    cmd[0] = COLOR_14_CLICK_PART_ID;
    ack1 = __i2c->write(COLOR_14_CLICK_ADD << 1, cmd, 1, true);
    ack2 = __i2c->read(COLOR_14_CLICK_ADD << 1, data, 1);
    if(DEBUG_MODE)  printf("Part ID Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("Part ID Acq (R) = %d\r\n", ack2);
    return data[0];
}

int Color_14_Click::getMainStatus(void){
    cmd[0] = COLOR_14_CLICK_MAIN_STAT;
    ack1 = __i2c->write(COLOR_14_CLICK_ADD << 1, cmd, 1, true);
    ack2 = __i2c->read(COLOR_14_CLICK_ADD << 1, data, 1);
    if(DEBUG_MODE)  printf("Main Status Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("Main Status Acq (R) = %d\r\n", ack2);
    return data[0];
}

void Color_14_Click::setGainRGB(int val){
    cmd[0] = COLOR_14_CLICK_LS_GAIN;
    cmd[1] = val;
    ack1 = __i2c->write(COLOR_14_CLICK_ADD << 1, cmd, 2);
    if(DEBUG_MODE)  printf("Gain Acq (W) = %d\r\n", ack1); 
}

int Color_14_Click::readRedValue(void){
    cmd[0] = COLOR_14_CLICK_RED_CHAN;
    ack1 = __i2c->write(COLOR_14_CLICK_ADD << 1, cmd, 1, true);
    ack2 = __i2c->read(COLOR_14_CLICK_ADD << 1, data, 3);
    if(DEBUG_MODE)  printf("Red Chan Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("Red Chan Acq (R) = %d\r\n", ack2);
    Red_color = (data[2] << 16) + (data[1] << 8) + data[0];
    return Red_color;
}

int Color_14_Click::readGreenValue(void){
    cmd[0] = COLOR_14_CLICK_GREEN_CHAN;
    ack1 = __i2c->write(COLOR_14_CLICK_ADD << 1, cmd, 1, true);
    ack2 = __i2c->read(COLOR_14_CLICK_ADD << 1, data, 3);
    if(DEBUG_MODE)  printf("Green Chan Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("Green Chan Acq (R) = %d\r\n", ack2);
    Green_color = (data[2] << 16) + (data[1] << 8) + data[0];
    return Green_color;
}

int Color_14_Click::readBlueValue(void){
    cmd[0] = COLOR_14_CLICK_BLUE_CHAN;
    ack1 = __i2c->write(COLOR_14_CLICK_ADD << 1, cmd, 1, true);
    ack2 = __i2c->read(COLOR_14_CLICK_ADD << 1, data, 3);
    if(DEBUG_MODE)  printf("Blue Chan Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("Blue Chan Acq (R) = %d\r\n", ack2);
    Blue_color = (data[2] << 16) + (data[1] << 8) + data[0];
    return Blue_color;
}


int Color_14_Click::readIRValue(void){
    cmd[0] = COLOR_14_CLICK_IR_CHAN;
    ack1 = __i2c->write(COLOR_14_CLICK_ADD << 1, cmd, 1, true);
    ack2 = __i2c->read(COLOR_14_CLICK_ADD << 1, data, 3);
    if(DEBUG_MODE)  printf("IR Chan Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("IR Chan Acq (R) = %d\r\n", ack2);
    IR_color = (data[2] << 16) + (data[1] << 8) + data[0];
    return IR_color;
}

void Color_14_Click::readRGBIRValue(int rgbIR[]){
    rgbIR[0] = readRedValue();
    rgbIR[1] = readGreenValue();
    rgbIR[2] = readBlueValue();
    rgbIR[3] = readIRValue();
}