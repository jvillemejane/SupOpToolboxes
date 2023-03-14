/**
 * FILENAME :        main_lib.h          
 *
 * DESCRIPTION :
 *       Robot 2 wheels / with Temp and Hum sensors.
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    13/mar/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */

#ifndef     __MAIN_LIB_H_HEADER_H__
#define     __MAIN_LIB_H_HEADER_H__

#include    "mbed.h"
#include    <string.h>
#include    "TEMPHUM_14_CLICK.h"
#include    "MOD24_NRF.h"
#include    "MCC_motor.h"
#define     WAIT_TIME_MS 500 

// For debugging
#define     DEBUG   1
extern      UnbufferedSerial    my_pc;
extern      char        charStr[];

// Temperature Sensor
extern      I2C         my_sensor_i2c;
extern      DigitalOut  my_sensor_reset;
extern      TempHum_14_Click    my_sensor;
// Value from the sensor
extern      float       temperature, humidity;
// Collected data
extern      float       temperatureI2C;
extern      uint8_t     temperatureBytes[];

// RF Transmission of data
#define         TRANSFER_SIZE   8
extern      nRF24L01P       nRF24_mod;
// MOSI, MISO, SCK, CSN, CE, IRQ
extern      char        dataToSend[];
extern      char        dataReceived[];



// Function to test conversion of data format
void        testConversion(void);
// Initialization function for the BT nRF24L01 module
//  frequency in MHz
void        initNRF24(int frequency);
// Receiving function for the BT nRF24L01 module
//  data : array of data received by the module
//  return the number of bytes received
uint8_t     receiveNRF24(char *data);
// Transmitting function for the BT nRF24L01 module
//  data : array of data to transmit
void        transmitNRF24(char *data);


#endif