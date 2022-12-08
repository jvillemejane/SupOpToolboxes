/**
 * FILENAME :        PMod_TC1.cpp          
 *
 * DESCRIPTION :
 *       PMod_TC1 / Temperature via Thermocouple Mode routines.
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    08/dec/2022
 *
 *       LEnsE / Institut d'Optique Graduate School
 */

 #include <mbed.h>
 #include "PMod_TC1.h"

PMod_TC1::PMod_TC1(SPI *_spi, DigitalOut _cs): __cs(_cs){
    __cs = 1;
    temperature_final = 0;
    temperature_thermo = 0;
    temperature_internal = 0;
    /* Initialisation of spi module */
    if (__spi){ delete _spi; }
    __spi=_spi;
    __spi->format(8,3);    // 32 bits are collected
    __spi->frequency(100000);   // Frequency of 100kHz
    thread_sleep_for(500);      // 500 ms
}


double PMod_TC1::readTemperature(void){
    temperature_final = 0;
    int k = readRawData();
    // internal value of temperature
    temperature_internal = ((k >> 4) & 0x0FFF) / 16.0;
    // sign of the temperature   
    if( (k & 0x00008000) == 0x00008000  )  temperature_internal = -temperature_internal;
    // thermocouple value of temperature
    temperature_thermo = ((k >> 17) & 0x3FFF) / 4.0;
    // sign of the temperature   
    if( (k & 0x80000000) == 0x80000000  )  temperature_thermo = -temperature_thermo; 
    // global value of the temperature
    temperature_final = temperature_thermo - temperature_internal;
    return temperature_final;
}

int PMod_TC1::readRawData(void){
    int k = 0;
    short k1, k2, k3, k4;
    __cs = 0;
    k1 = __spi->write(0);
    k2 = __spi->write(0);
    k3 = __spi->write(0);
    k4 = __spi->write(0);
    __cs = 1;
    k = (k1 << 24) + (k2 << 16) + (k3 << 8) + k4;
    return k;
}

double PMod_TC1::getInternalTemperature(void){
    int k = readRawData();
    double t = ((k >> 4) & 0x0FFF);
    if( (k & 0x00008000) == 0x00008000  )  t = -t;  // sign of the temperature
    return t / 16.0;
}

double PMod_TC1::getThermoTemperature(void){
    int k = readRawData();
    double t = ((k >> 17) & 0x3FFF);
    if( (k & 0x80000000) == 0x80000000  )  t = -t;  // sign of the temperature
    return t / 4.0;
}