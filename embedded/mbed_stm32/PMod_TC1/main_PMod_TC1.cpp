/**
 * FILENAME :        main_PMod_TC1.cpp          
 *
 * DESCRIPTION :
 *       PMod_TC1 / Temperature via Thermocouple Mode main code.
 *		 required : PMod_TC1 library for MBED OS 6
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    08/dec/2022
 *
 *       LEnsE / Institut d'Optique Graduate School
 */

#include "mbed.h"
#include "PMod_TC1.h"

#define WAIT_TIME_MS 500 

/// Create a SPI interface with specific pins : Mosi, Miso, Sclk
SPI spi_module(D11, D12, D13);
/// Create a PMod_TC1 module connection with a SPI interface and a Slave Select pin
PMod_TC1 module(&spi_module, D10);

int main()
{
    double temperature = 0;
    int raw_temp = 0;

    printf("MBED bare metal OS %d.%d.%d.\r\n", MBED_MAJOR_VERSION, MBED_MINOR_VERSION, MBED_PATCH_VERSION);
    printf("\tPmod_TC1 functions test\r\n");
    printf("\tby LEnsE / Villou\r\n");

    while (true)
    {
        printf("\tTint = %lf\r\n", module.getInternalTemperature());
        printf("\tTthe = %lf\r\n", module.getThermoTemperature());
        printf("\tTraw = %x\r\n", module.readRawData());
        printf("Tfinal = %lf\r\n", module.readTemperature());
        thread_sleep_for(WAIT_TIME_MS);
    }
}
