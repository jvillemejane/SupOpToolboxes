/**
 * FILENAME :        COLOR_10_CLICK.cpp          
 *
 * DESCRIPTION :
 *       COLOR_10_CLICK / RGB Sensor from MikroE.
 *
 *       This module allows to measure Red Green and Blue light intensity (and IR)
 *  with a specific I2C device - VEML-3328 from Vishay
 *       !! Each I2C data are on 2 bytes !!
 *       More informations : https://www.vishay.com/product/84968/
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    07/feb/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */


 #include <mbed.h>
 #include "COLOR_10_CLICK.h"

Color_10_Click::Color_10_Click(I2C *_i2c, DigitalOut *_led_data){
    /* Initialisation of interrupt input */
    if (_led_data){ delete __led_data; }
    __led_data = _led_data;
    __led = new WS2812(__led_data, 1, 0, 5, 5, 0);  // only 1 _led_data
        // Timing value 0,5,5,0 are for L476RG Nucleo Board
    __led->useGlobalBrightness(false);
    __led->SetAll(0);  // Led Off at the beginning
    /* Initialisation of i2c module */
    if (_i2c){ delete __i2c; }
    __i2c=_i2c;
    __i2c->frequency(400000);   // Frequency of 400kHz
    thread_sleep_for(10);      // 10 ms
}

void Color_10_Click::powerUp(void){
    cmd[0] = COLOR_10_CLICK_COMMAND;
    cmd[1] = 0;
    cmd[2] = 0;
    ack1 = __i2c->write(COLOR_10_CLICK_ADD << 1, cmd, 3);
    if(DEBUG_MODE) printf("Init Acq = %d\r\n", ack1);
    wait_us(1000);
}

int Color_10_Click::getPartID(void){
    // Part ID Status
    cmd[0] = COLOR_10_CLICK_PART_ID;
    ack1 = __i2c->write(COLOR_10_CLICK_ADD << 1, cmd, 1, true);
    ack2 = __i2c->read(COLOR_10_CLICK_ADD << 1, data, 2);
    if(DEBUG_MODE)  printf("Part ID Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("Part ID Acq (R) = %d\r\n", ack2);
    return data[0];
}


int Color_10_Click::getCommandValue(void){
    cmd[0] = COLOR_10_CLICK_COMMAND;
    ack1 = __i2c->write(COLOR_10_CLICK_ADD << 1, cmd, 1, true);
    ack2 = __i2c->read(COLOR_10_CLICK_ADD << 1, data, 2);
    if(DEBUG_MODE)  printf("Command Value Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("Command Value Acq (R) = %d\r\n", ack2);
    return (data[1] << 8) + data[0];
}

void Color_10_Click::setGainRGB(int val){
    int command_value = getCommandValue();
    cmd[0] = COLOR_10_CLICK_COMMAND;
    cmd[1] = (command_value & 0xFF);
    cmd[2] = ((command_value >> 8) & 0b11110011) | (val << 2);
    ack1 = __i2c->write(COLOR_10_CLICK_ADD << 1, cmd, 3);
    if(DEBUG_MODE)  printf("Gain Acq (W) = %d\r\n", ack1); 
}

int Color_10_Click::readRedValue(void){
    cmd[0] = COLOR_10_CLICK_RED_CHAN;
    ack1 = __i2c->write(COLOR_10_CLICK_ADD << 1, cmd, 1, true);
    ack2 = __i2c->read(COLOR_10_CLICK_ADD << 1, data, 2);
    if(DEBUG_MODE)  printf("Red Chan Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("Red Chan Acq (R) = %d\r\n", ack2);
    Red_color = (data[1] << 8) + data[0];
    return Red_color;
}

int Color_10_Click::readGreenValue(void){
    cmd[0] = COLOR_10_CLICK_GREEN_CHAN;
    ack1 = __i2c->write(COLOR_10_CLICK_ADD << 1, cmd, 1, true);
    ack2 = __i2c->read(COLOR_10_CLICK_ADD << 1, data, 2);
    if(DEBUG_MODE)  printf("Green Chan Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("Green Chan Acq (R) = %d\r\n", ack2);
    Green_color = (data[1] << 8) + data[0];
    return Green_color;
}

int Color_10_Click::readBlueValue(void){
    cmd[0] = COLOR_10_CLICK_BLUE_CHAN;
    ack1 = __i2c->write(COLOR_10_CLICK_ADD << 1, cmd, 1, true);
    ack2 = __i2c->read(COLOR_10_CLICK_ADD << 1, data, 2);
    if(DEBUG_MODE)  printf("Blue Chan Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("Blue Chan Acq (R) = %d\r\n", ack2);
    Blue_color = (data[1] << 8) + data[0];
    return Blue_color;
}

int Color_10_Click::readIRValue(void){
    cmd[0] = COLOR_10_CLICK_IR_CHAN;
    ack1 = __i2c->write(COLOR_10_CLICK_ADD << 1, cmd, 1, true);
    ack2 = __i2c->read(COLOR_10_CLICK_ADD << 1, data, 2);
    if(DEBUG_MODE)  printf("IR Chan Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("IR Chan Acq (R) = %d\r\n", ack2);
    IR_color = (data[1] << 8) + data[0];
    return IR_color;
}

int Color_10_Click::readClearValue(void){
    cmd[0] = COLOR_10_CLICK_CLEAR_CHAN;
    ack1 = __i2c->write(COLOR_10_CLICK_ADD << 1, cmd, 1, true);
    ack2 = __i2c->read(COLOR_10_CLICK_ADD << 1, data, 2);
    if(DEBUG_MODE)  printf("Clear Chan Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("Clear Chan Acq (R) = %d\r\n", ack2);
    Clear_color = (data[1] << 8) + data[0];
    return Clear_color;
}

void Color_10_Click::readRGBCIRValue(int rgbcIR[]){
    rgbcIR[0] = readRedValue();
    rgbcIR[1] = readGreenValue();
    rgbcIR[2] = readBlueValue();
    rgbcIR[3] = readClearValue();
    rgbcIR[4] = readIRValue();
}

void Color_10_Click::setLedWhite(char ww){
    __led->SetAll(0x00FFFFFF * (ww / 255.0));
    __led->write();
}

void Color_10_Click::setLedRed(char rr){
    __led->SetAll(0x00FF0000 * (rr / 255.0));
    __led->write();
}

void Color_10_Click::setLedBlue(char bb){
    __led->SetAll(0x000000FF * (bb / 255.0));
    __led->write();
}

void Color_10_Click::setLedGreen(char gg){
    __led->SetAll(0x0000FF00 * (gg / 255.0));
    __led->write();
}

void Color_10_Click::setLedOff(void){
    __led->SetAll(0);
    __led->write();
}