/**
 * FILENAME :        PMod_TC1.h          
 *
 * DESCRIPTION :
 *       PMod_TC1 / Temperature via Thermocouple Mode routines.
 *
 *       This module allows to measure a temperature
 *  with an accurate thermocouple (14-bit ADC resolution)
 *       More informations : https://digilent.com/reference/_media/reference/pmod/pmodtc1/pmodtc1_rm.pdf
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    08/dec/2022
 *
 *       LEnsE / Institut d'Optique Graduate School
 */

#ifndef __PMOD_TC1_HEADER_H__
#define __PMOD_TC1_HEADER_H__

#include <mbed.h>

/**
 * @class PMod_TC1
 * @brief Access to the PMod_TC1 module from Digilent
 * @details     PMod_TC1 module allows to measure a temperature
 *  with an accurate thermocouple.
 *      The thermocouple measure is collected by a 14-bit ADC
 *      Temperature range : -73deg to 482deg
 *      VOUT = (41.276 μV/°C) × (TR - TAMB)
 */
class PMod_TC1{
    private:
        /// Converted temperature of the thermocouple.
        double temperature_thermo;
        /// Converted internal temperature for comparaison.
        double temperature_internal;
        /// Final temperature 
        double temperature_final;
        
        /// SPI interface pins 
        SPI *__spi = NULL;
        /// Slave Select pin
        DigitalOut __cs;


    public:
        /**
        * @brief Simple constructor of the PMod_TC1 class.
        * @details Create a PMod_TC1 object with
        *    an SPI interface and a Slave Select pin
        *    SPI communication will be initialized at 100kHz
        * @param _spi SPI interface not initialized
        * @param _cs Slave Select pin connected to the module
        */
        PMod_TC1(SPI *_spi, DigitalOut _cs);

        /**
        * @brief Read the data from the PMod_TC1 module
        * @details Read the data from the PMod_TC1 module
        *   and update the member value of the object - 
        *
        * @return the final temperature.
        */
        double readTemperature(void);

        /**
        * @brief Read the raw data from the PMod_TC1 module
        *
        * @return the raw value.
        */
        int readRawData(void);

        /**
        * @brief Get the internal temperature of the module
        *
        * @return the internal temperature of the module.
        */
        double getInternalTemperature(void);

        /**
        * @brief Get the thermocouple temperature of the module
        *
        * @return the thermocouple temperature of the module.
        */
        double getThermoTemperature(void);
};


#endif