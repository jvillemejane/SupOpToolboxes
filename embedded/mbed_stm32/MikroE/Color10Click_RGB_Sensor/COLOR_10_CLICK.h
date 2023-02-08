/**
 * FILENAME :        COLOR_10_CLICK.h          
 *
 * DESCRIPTION :
 *       COLOR_10_CLICK / RGB Sensor from MikroE.
 *
 *       This module allows to measure Red Green and Blue light intensity (and IR)
 *  with a specific I2C device - VEML-3328 from Vishay
 *       !! Each I2C data are on 2 bytes !!
 *       More informations : https://www.vishay.com/product/84968/
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    07/feb/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */
#ifndef __COLOR_10_CLICK_HEADER_H__
#define __COLOR_10_CLICK_HEADER_H__

#include <mbed.h>
#include "WS2812.h"
 
/** Constant definition */
#define     DEBUG_MODE                  1

#define     COLOR_10_CLICK_ADD          0x10
#define     COLOR_10_CLICK_COMMAND      0x00
#define     COLOR_10_CLICK_PART_ID      0x0C
#define     COLOR_10_CLICK_CLEAR_CHAN   0x04
#define     COLOR_10_CLICK_RED_CHAN     0x05
#define     COLOR_10_CLICK_GREEN_CHAN   0x06
#define     COLOR_10_CLICK_BLUE_CHAN    0x07
#define     COLOR_10_CLICK_IR_CHAN      0x08

#define     COLOR_10_CLICK_GAIN_1_2x    0b11
#define     COLOR_10_CLICK_GAIN_1x      0b00        // default value
#define     COLOR_10_CLICK_GAIN_2x      0b01
#define     COLOR_10_CLICK_GAIN_4x      0b10


/**
 * @class Color_10_Click
 * @brief Access to the Color10Click module from MikroE
 * @details     Color10Click module allows to measure RGB light intensities
 *  with a VEML-3328 sensor from Vishay.
 */
class Color_10_Click{
     private:
        /// Intensity of the Red component
        int     Red_color;
        /// Intensity of the Green component
        int     Green_color;
        /// Intensity of the Blue component
        int     Blue_color;
        /// Global intensity 
        int     Clear_color;
        /// Intensity of the InfraRed component
        int     IR_color;
        /// Command to send
        char    cmd[3];
        /// Received Data
        char    data[2];
        /// Acknowledgement variables
        char    ack1, ack2;
        
        /// I2C interface pins 
        I2C             *__i2c = NULL;
        /// digital output to control the WS2812 RGB Led
        DigitalOut      *__led_data = NULL;
        /// WS2812 led
        WS2812          *__led;

    public:
        /**
        * @brief Simple constructor of the Color_10_Click class.
        * @details Create a Color_10_Click object with
        *    an I2C interface
        *    I2C communication will be initialized at 400kHz
        * @param _i2c SPI interface not initialized
        * @param _led_data digital output to control the WS2812 RGB Led 
        */
        Color_10_Click(I2C *_i2c, DigitalOut *_led_data);

        /**
        * @brief Initiatlization of the sensor
        * @details Initialize the sensor
        */
        void powerUp(void);

        /**
        * @brief Return the ID of the module
        * @return the part ID of the module - default 0x28 = 40d
        */
        int getPartID(void);

        /**
        * @brief Return the value of the Command register
        * @return the value of the Command register
        */
        int getCommandValue(void);

        /**
        * @brief Set the analog gain of the sensor
        * @details Gain in range : 1/2x, 1x (default), 2x, 4x
        * @param val gain value - COLOR_10_CLICK_GAIN_1X
        */
        void setGainRGB(int val);

        /**
        * @brief Read the red data from the Color_10_Click module
        * @details Read the red data from the Color_10_Click module
        *   and update the member value of the object - 
        *
        * @return the Red component of the light.
        */
        int readRedValue(void);

        /**
        * @brief Read the green data from the Color_10_Click module
        * @details Read the green data from the Color_10_Click module
        *   and update the member value of the object - 
        *
        * @return the Green component of the light.
        */
        int readGreenValue(void);

        /**
        * @brief Read the blue data from the Color_10_Click module
        * @details Read the blue data from the Color_10_Click module
        *   and update the member value of the object - 
        *
        * @return the Blue component of the light.
        */
        int readBlueValue(void);

        /**
        * @brief Read the InfraRed data from the Color_10_Click module
        * @details Read the infrared data from the Color_10_Click module
        *   and update the member value of the object - 
        *
        * @return the IR component of the light.
        */
        int readIRValue(void);

        /**
        * @brief Read the Clear data from the Color_10_Click module
        * @details Read the clear data from the Color_10_Click module
        *   and update the member value of the object - 
        *
        * @return the clear component of the light.
        */
        int readClearValue(void);

        /**
        * @brief Collect all the RGBIR data from the Color_10_Click module
        * @details Read all the RGBIR data from the Color_10_Click module
        *   and update the members value of the object - 
        *
        * @param rgbcIR first cell of a 5 int arrays
        * @return R G B C IR value in a 5 int arrays
        */
        void readRGBCIRValue(int rgbcIR[]);

        void setLedWhite(char ww);
        void setLedRed(char rr);
        void setLedBlue(char bb);
        void setLedGreen(char gg);
        void setLedOff(void);
};

#endif