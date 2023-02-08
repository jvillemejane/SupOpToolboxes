/**
 * FILENAME :        main_Color_10_Click.cpp          
 *
 * DESCRIPTION :
 *       Color_10_Click / RGB Sensor Library Testing.
 *		 required : Color_10_Click library for MBED OS 6
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    08/feb/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */

#include "mbed.h"
#include "COLOR_10_CLICK.h"

#define WAIT_TIME_MS 500 
DigitalOut led1(LED1);

/// Create an I2C interface with specific pins : SDA / SCL
I2C                 my_color_i2c(D14, D15); // SDA / SCL

/// Create a digital output for WS2812 RGB Led
DigitalOut          my_led(D9);
/// Create a Color_10_Click module connection with an I2C interface and a Digital Out for the led
Color_10_Click      my_sensor_(&my_color_i2c, &my_led);

/// Create a 5 integers array to collect R, G, B, clear and IR data from the sensor
int             RGBCir[5] = {0};


int main()
{
    int k = 0;
    printf("Test.\n");
    /// PowerUp and initialize the module in automode
    my_sensor_.powerUp();
    /// Collect informations about the sensor
    printf("Part ID = %d\r\n", my_sensor_.getPartID());
    printf("Command = %d\r\n", my_sensor_.getCommandValue());

    /// Modify the analog gain of the sensor - 3x by default
    my_sensor_.setGainRGB(COLOR_10_CLICK_GAIN_2x);


    while (true)
    {
        k++;
        led1 = !led1;
        /// Collect R, G, B, Clear and IR data from the sensor
        my_sensor_.readRGBCIRValue(RGBCir);
        printf("[%4d] R=%d / G=%d / B=%d / C=%d / IR = %d \r\n\n ", k, RGBCir[0], RGBCir[1], RGBCir[2], RGBCir[3], RGBCir[4]);
        /// Every 0.5s
        thread_sleep_for(WAIT_TIME_MS);
    }
}

