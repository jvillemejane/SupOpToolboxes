/**
 * FILENAME :        main_WS2812.cpp          
 *
 * DESCRIPTION :
 *       WS2812 / Intelligent control LED integrated light source Library Testing.
 *		 required : WS2812 library for MBED OS 6
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    07/feb/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */

#include "mbed.h"
#include "WS2812.h"
#define     LED_STRIP_NB        6

#define WAIT_TIME_MS 500 
DigitalOut led1(LED1);

/// Create a digital output for WS2812 RGB Led
DigitalOut smart_led(D9);
/// Create a WS2812 module - Timing is for L476RG Nucleo Board
WS2812 ws(&smart_led, LED_STRIP_NB, 0, 5, 5, 0);


int main()
{
    int k = 0;
    int gb = 100;
    ws.SetAll(0);       // Clear All
    ws.SetAllB(200);                // Init in Blue
    ws.write();                     // Send Data to strip
    thread_sleep_for(500);         // ... wait 0.5s

    while (true)
    {
        k++;
        led1 = !led1;
        ws.SetAll(0);       // Clear All
        if(k%2 == 0)        // 1 time on 2...
            ws.SetAllR(200);    // Led in Blue
        else
            ws.SetAllB(150);    // Led in Green
        ws.write();
        /// Every 0.5s
        thread_sleep_for(WAIT_TIME_MS);
    }
}
