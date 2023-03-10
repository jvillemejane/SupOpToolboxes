/**
 * FILENAME :        TEMPHUM_14_CLICK.h          
 *
 * DESCRIPTION :
 *       TEMPHUM_14_CLICK / Temperature and Humidity sensors from MikroE.
 *
 *       This module allows to measure Temperature and Humidity
 *  with a specific I2C device - HTU31 from TE Connectivity
 *       More informations : https://www.te.com/usa-en/product-CAT-HSC0007.html
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    09/feb/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */
#ifndef __TEMPHUM_14_CLICK_HEADER_H__
#define __TEMPHUM_14_CLICK_HEADER_H__

#include <cstdint>
#include <mbed.h>
 
/** Constant definition */
#define     DEBUG_MODE                  1

#define     TEMPHUM_14_CLICK_ADD            0x40
#define     TEMPHUM_14_CLICK_PART_ID        0x0A
#define     TEMPHUM_14_CLICK_DIAG           0x08
#define     TEMPHUM_14_CLICK_CONV           0x40
#define     TEMPHUM_14_CLICK_READ_T_RH      0x00
#define     TEMPHUM_14_CLICK_READ_RH        0x10
#define     TEMPHUM_14_CLICK_RESET          0x1E
#define     TEMPHUM_14_CLICK_HEAT_ON        0x04
#define     TEMPHUM_14_CLICK_HEAT_OFF       0x02


/**
 * @class TempHum_14_Click
 * @brief Access to the Temp&Hum14Click module from MikroE
 * @details     Temp&Hum14Click module allows to measure temperature and humidity
 *  with a HTU31 sensor from TEConnectivity.
 */
class TempHum_14_Click{
     private:
        /// Temperature
        float   _temperature;
        /// Humidity
        float   _humidity;

        /// Command to send
        char    cmd[2];
        /// Received Data
        char    data[6];
        /// Acknowledgement variables
        char    ack1, ack2;
        
        /// I2C interface pins 
        I2C             *__i2c = NULL;
        /// reset input of the HTU31
        DigitalOut      *__reset = NULL;

    public:
        /**
        * @brief Simple constructor of the TempHum_14_Click class.
        * @details Create a TempHum_14_Click object with
        *    an I2C interface
        *    I2C communication will be initialized at 400kHz
        * @param _i2c SPI interface not initialized
        * @param _rst reset input of the HTU31 
        */
        TempHum_14_Click(I2C *_i2c, DigitalOut *_rst);

        /**
        * @brief Reset of the sensor
        * @details Reset of the sensor / 5 ms
        */
        void resetSensor(void);

        /**
        * @brief Return the ID of the module
        * @return the part ID of the module - default 11536906(d)
        */
        int getPartID(void);

        /**
        * @brief Return the value of the DIAG register of the module
        * @return the value of the DIAG register of the module - default ??
        */
        int getDiag(void);

        /**
        * @brief Read the temperature and the humidity data from the Temp&Hum_14_Click module
        * @details Read the temperature and the humidity data from the Color_14_Click module
        *   and update the members value of the object - 
        *
        * @param temp Pointer to the temperature variable.
        * @param hum Pointer to the humidity variable.
        * @return Temperature and Humidity from the sensor.
        */
        void readTRH(float *temp, float *hum);

        /**
        * @brief Convert a float value to a 4 bytes array
        *
        * @param value Floating variable to convert.
        * @param value Array of 4 bytes.
        */
        void floatToBytes(float *value, uint8_t xbuf[]);

        /**
        * @brief Convert a 4 bytes array to a floating variable
        *
        * @param xbuf Pointer to a 4 bytes array.
        * @return Floating value.
        */
        float bytesToFloat(uint8_t xbuf[]);
};

#endif