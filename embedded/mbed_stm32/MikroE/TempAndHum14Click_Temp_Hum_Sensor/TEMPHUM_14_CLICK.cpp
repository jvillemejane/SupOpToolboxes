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

 #include <mbed.h>
 #include "TEMPHUM_14_CLICK.h"

TempHum_14_Click::TempHum_14_Click(I2C *_i2c, DigitalOut *_rst){
    /* Initialisation of interrupt input */
    if (_rst){ delete __reset; }
    __reset=_rst;
    /* Initialisation of i2c module */
    if (_i2c){ delete __i2c; }
    __i2c=_i2c;
    __i2c->frequency(400000);   // Frequency of 400kHz
    thread_sleep_for(10);      // 10 ms
}

void TempHum_14_Click::resetSensor(void){
    cmd[0] = TEMPHUM_14_CLICK_RESET;
    ack1 = __i2c->write(TEMPHUM_14_CLICK_ADD << 1, cmd, 1);
    if(DEBUG_MODE) printf("Reset Acq = %d\r\n", ack1);
    thread_sleep_for(20);    // 20 ms
}

int TempHum_14_Click::getPartID(void){
    // Part ID Status / 4 bytes
    cmd[0] = TEMPHUM_14_CLICK_PART_ID;
    ack1 = __i2c->write(TEMPHUM_14_CLICK_ADD << 1, cmd, 1);
    ack2 = __i2c->read(TEMPHUM_14_CLICK_ADD << 1, data, 4);
    if(DEBUG_MODE)  printf("Part ID Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("Part ID Acq (R) = %d\r\n", ack2);
    return (data[2] << 16) + (data[0] << 8) + (data[0]);
}

int TempHum_14_Click::getDiag(void){
    // Diagnostic Register / 1 byte
    cmd[0] = TEMPHUM_14_CLICK_DIAG;
    ack1 = __i2c->write(TEMPHUM_14_CLICK_ADD << 1, cmd, 1);
    ack2 = __i2c->read(TEMPHUM_14_CLICK_ADD << 1, data, 1);
    if(DEBUG_MODE)  printf("Diag Acq (W) = %d\r\n", ack1);
    if(DEBUG_MODE)  printf("Diag Acq (R) = %d\r\n", ack2);
    return data[0];
}

void TempHum_14_Click::readTRH(float *temp, float *hum){
    // Conversion in fast mode    
    cmd[0] = TEMPHUM_14_CLICK_CONV;
    ack1 = __i2c->write(TEMPHUM_14_CLICK_ADD << 1, cmd, 1);
    if(DEBUG_MODE)  printf("Conv Acq (W) = %d\r\n", ack1);
    thread_sleep_for(3);    // 3 ms   
    // Read data    
    cmd[0] = TEMPHUM_14_CLICK_READ_T_RH;
    ack1 = __i2c->write(TEMPHUM_14_CLICK_ADD << 1, cmd, 1);
    ack2 = __i2c->read(TEMPHUM_14_CLICK_ADD << 1, data, 6);
    int tEmp = (data[0] << 8) + (data[1]);
    int hUm = (data[0] << 8) + (data[1]);
    _temperature = -40.0 + 165.0 * tEmp / 65535;
    *temp = _temperature;    
    _humidity = 100.0 * hUm / 65535;
    *hum = _humidity;
}

void TempHum_14_Click::floatToBytes(float *value, uint8_t xbuf[]) {
    uint8_t *b = (uint8_t*) value;
    memcpy(xbuf,b,sizeof(xbuf));
}

float TempHum_14_Click::bytesToFloat(uint8_t xbuf[]) {
    float x = *((float*)(xbuf));
    return x;
}

