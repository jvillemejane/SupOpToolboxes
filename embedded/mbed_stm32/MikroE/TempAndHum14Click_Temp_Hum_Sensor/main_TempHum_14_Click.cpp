/**
 * FILENAME :        main_TempHum_14_Click.cpp          
 *
 * DESCRIPTION :
 *       TempHum_14_Click / Temperature and Humidity Sensor Library Testing.
 *		 required : TempHum_14_Click library for MBED OS 6
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    09/feb/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */

#include "mbed.h"
#include "TEMPHUM_14_CLICK.h"


#define WAIT_TIME_MS 500 
DigitalOut led1(LED1);

/// Create an I2C interface with specific pins : SDA / SCL
I2C                 my_i2c(D14, D15); // SDA / SCL

/// Create a digital output for reset input of the sensor
DigitalOut          my_rst(D9);
/// Create a Color_10_Click module connection with an I2C interface and a Digital Out for the led
TempHum_14_Click    my_sensor(&my_i2c, &my_rst);

int main()
{
    int k = 0;
    float T, H;
    printf("Test.\n");
    thread_sleep_for(WAIT_TIME_MS);
    /// PowerUp and initialize the module
    my_sensor.resetSensor();
    /// Collect informations about the sensor
    printf("Part ID = %x\r\n", my_sensor.getPartID());
    printf("Diag = %x\r\n", my_sensor.getDiag());

    while (true)
    {
        k++;
        led1 = !led1;
        /// Collect T and H data from the sensor
        my_sensor.readTRH(&T, &H);
        printf("[%4d] T=%f / H=%f \r\n\n ", k, T, H);
        /// Every 0.5s
        thread_sleep_for(WAIT_TIME_MS);
    }
}
