/**
 * FILENAME :        WS2812.cpp          
 *
 * DESCRIPTION :
 *       WS2812 / RGB Led.
 *
 *       WS2812 Leds are Intelligent control LED integrated light source.
 *       More informations : https://cdn-shop.adafruit.com/datasheets/WS2812.pdf
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    07/feb/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */


 #include <mbed.h>
 #include "WS2812.h"

WS2812::WS2812(DigitalOut *led, int size, int zeroHigh, int zeroLow, int oneHigh, int oneLow)
{
    if (led){ delete __led; }
    __led = led;
    __size = size;
    __pBuf = new int[size];
    __transmitBuf = new bool[size * FRAME_SIZE];
    __use_GB = false;
    __GB = 0xFF; // set global intensity to full
    
    // Default values designed for K64f. Assumes GPIO toggle takes ~0.4us
    setDelays(zeroHigh, zeroLow, oneHigh, oneLow);
}

WS2812::~WS2812()
{
    delete[] __transmitBuf;
    delete[] __pBuf;
}

void WS2812::setDelays(int zeroHigh, int zeroLow, int oneHigh, int oneLow) {
    __zeroHigh = zeroHigh;
    __zeroLow = zeroLow;
    __oneHigh = oneHigh;
    __oneLow = oneLow;
}

void WS2812::__loadBuf(int r_offset, int g_offset, int b_offset) {
    for (int i = 0; i < __size; i++) {
        int color = 0;
               
        color |= ((__pBuf[(i+g_offset)%__size] & 0x0000FF00));
        color |= ((__pBuf[(i+r_offset)%__size] & 0x00FF0000));
        color |=  (__pBuf[(i+b_offset)%__size] & 0x000000FF);
        color |= (__pBuf[i] & 0xFF000000);
        
        // Outut format : GGRRBB
        // Inout format : IIRRGGBB
        unsigned char agrb[4] = {0x0, 0x0, 0x0, 0x0};
    
        unsigned char sf; // scaling factor for  GB
    
        // extract colour fields from incoming
        // 0 = green, 1 = red, 2 = blue, 3 = brightness        
        agrb[0] = (color & 0x0000FF00) >> 8;
        agrb[1] = (color & 0x00FF0000) >> 16;
        agrb[2] = color  & 0x000000FF;
        agrb[3] = (color & 0xFF000000) >> 24;
    
        // set the intensity scaling factor (global, per pixel, none)
        if (__use_GB == true) {
            sf = __GB;
        } else {
            sf = 0xFF;
        }
        
        // Apply the scaling factor to each other colour components
        for (int clr = 0; clr < 3; clr++) {
            agrb[clr] = ((agrb[clr] * sf) >> 8);
            
            for (int j = 0; j < 8; j++) {
                if (((agrb[clr] << j) & 0x80) == 0x80) {
                    // Bit is set (checks MSB fist)
                    __transmitBuf[(i * FRAME_SIZE) + (clr * 8) + j] = 1;
                } else {
                    // Bit is clear
                    __transmitBuf[(i * FRAME_SIZE) + (clr * 8) + j] = 0;
                }
            }
        }
    }
}

void WS2812::write(void) {
    write_offsets(0, 0, 0);
}

void WS2812::write_offsets (int r_offset, int g_offset, int b_offset) {
    int i, j;
    
    // Load the transmit buffer
    __loadBuf(r_offset, g_offset, b_offset);

    // Entering timing critical section, so disabling interrupts
    __disable_irq();
    
    // Begin bit-banging
    for (i = 0; i < FRAME_SIZE * __size; i++) {
        j = 0;
        if (__transmitBuf[i]){
            *__led = 1;
            for (; j < __oneHigh; j++) {
                __nop();
            }
            *__led = 0;
            for (; j < __oneLow; j++) {
                __nop();
            }
        } else {
            *__led = 1;
            for (; j < __zeroHigh; j++) {
                __nop();
            }
            *__led = 0;
            for (; j < __zeroLow; j++) {
                __nop();
            }
        }
    }
    
    // Exiting timing critical section, so enabling interrutps
    __enable_irq();
}

void WS2812::useGlobalBrightness(bool gb)
{
    __use_GB = gb;
}

void WS2812::setGlobalBrightness(unsigned char GB)
{
    __GB = GB;
}

void WS2812::SetAll(unsigned int value)
{
    // for each pixel
    for (int i=0 ; i < __size; i++) {
        __set_pixel(i,value);
    }
}

void WS2812::SetAllI(unsigned char value)
{
    // for each pixel
    for (int i=0 ; i < __size; i++) {
        __set_pixel_component(i,3,value);
    }
}

void WS2812::SetAllR(unsigned char value)
{
    // for each pixel
    for (int i=0 ; i < __size; i++) {
        __set_pixel_component(i,2,value);
    }
}

void WS2812::SetAllG(unsigned char value)
{
    // for each pixel
    for (int i=0 ; i < __size; i++) {
        __set_pixel_component(i,1,value);
    }
}

void WS2812::SetAllB(unsigned char value)
{
    // for each pixel
    for (int i=0 ; i < __size; i++) {
        __set_pixel_component(i,0,value);
    }
}

void WS2812::Set(int i, unsigned int value)
{
    if ((i >= 0) && (i < __size)) {
        __set_pixel(i,value);
    }
}

void WS2812::SetI(int i, unsigned char value)
{
    if ((i >= 0) && (i < __size)) {
        __set_pixel_component(i,3,value);
    }
}


void WS2812::SetR(int i, unsigned char value)
{
    if ((i >= 0) && (i < __size)) {
        __set_pixel_component(i,2,value);
    }
}

void WS2812::SetG(int i, unsigned char value)
{
    if ((i >= 0) && (i < __size)) {
        __set_pixel_component(i,1,value);
    }
}

void WS2812::SetB(int i, unsigned char value)
{
    if ((i >= 0) && (i < __size)) {
        __set_pixel_component(i,0,value);
    }
}


int* WS2812::getBuf()
{
    return (__pBuf);
}


// set either the I,R,G,B value of specific pixel channel
void WS2812::__set_pixel_component(int index, int channel, int value)
{

    // AND with 0x00 shifted to the right location to clear the bits
    __pBuf[index] &= ~(0xFF << (8 * channel));

    // Set the bits with an OR
    __pBuf[index] |= (value << (8 * channel));
}


// set either the I,R,G,B value of specific pixel channel
void WS2812::__set_pixel(int index, int value)
{
    // AND with 0x00 shifted to the right location to clear the bits
    __pBuf[index] = value;
}