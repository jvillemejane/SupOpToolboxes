/**
 * FILENAME :        COLOR_14_CLICK.h          
 *
 * DESCRIPTION :
 *       COLOR_14_CLICK / RGB Sensor from MikroE.
 *
 *       This module allows to measure Red Green and Blue light intensity (and IR)
 *  with a specific I2C device - APDS-9151 from BroadCom
 *       More informations : https://www.broadcom.com/products/optical-sensors/integrated-ambient-light-and-proximity-sensors/apds-9151
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    07/feb/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */
#ifndef __COLOR_14_CLICK_HEADER_H__
#define __COLOR_14_CLICK_HEADER_H__

#include <mbed.h>
 
/** Constant definition */
#define     DEBUG_MODE                  1

#define     COLOR_14_CLICK_ADD          0x52
#define     COLOR_14_CLICK_MAIN_CTRL    0x00
#define     COLOR_14_CLICK_PART_ID      0x06
#define     COLOR_14_CLICK_MAIN_STAT    0x07
#define     COLOR_14_CLICK_RED_CHAN     0x13
#define     COLOR_14_CLICK_GREEN_CHAN   0x0D
#define     COLOR_14_CLICK_BLUE_CHAN    0x10
#define     COLOR_14_CLICK_IR_CHAN      0x0A
#define     COLOR_14_CLICK_LS_GAIN      0x05

#define     COLOR_14_CLICK_LS_GAIN_1X   0x00
#define     COLOR_14_CLICK_LS_GAIN_3X   0x01
#define     COLOR_14_CLICK_LS_GAIN_6X   0x02
#define     COLOR_14_CLICK_LS_GAIN_9X   0x03
#define     COLOR_14_CLICK_LS_GAIN_18X  0x04



/**
 * @class Color_14_Click
 * @brief Access to the Color14Click module from MikroE
 * @details     Color14Click module allows to measure RGB light intensities
 *  with a APDS-9151 sensor from BroadCom.
 */
class Color_14_Click{
     private:
        /// Intensity of the Red component
        int     Red_color;
        /// Intensity of the Green component
        int     Green_color;
        /// Intensity of the Blue component
        int     Blue_color;
        /// Intensity of the InfraRed component
        int     IR_color;
        /// Command to send
        char    cmd[2];
        /// Received Data
        char    data[3];
        /// Acknowledgement variables
        char    ack1, ack2;
        
        /// I2C interface pins 
        I2C             *__i2c = NULL;
        /// interrupt Input pin
        InterruptIn     *__int = NULL;

    public:
        /**
        * @brief Simple constructor of the Color_14_Click class.
        * @details Create a Color_14_Click object with
        *    an I2C interface
        *    I2C communication will be initialized at 400kHz
        * @param _i2c SPI interface not initialized
        * @param _int interrupt Input 
        */
        Color_14_Click(I2C *_i2c, InterruptIn *_int);

        /**
        * @brief Initiatlization of the sensor
        * @details Initialize the sensor
        */
        void powerUp(void);

        /**
        * @brief Initiatlization in RGB Mode only
        * @details Initialize the sensor in RGB Mode only
        */
        void initRGBSensor(void);

        /**
        * @brief Return the ID of the module
        * @return the part ID of the module - default 0xC2 = 194d
        */
        int getPartID(void);

        /**
        * @brief Return the status of the module
        * @return the part status of the module - default 0x20 = 32d or 0x00
        */
        int getMainStatus(void);

        /**
        * @brief Set the analog gain of the sensor
        * @details Gain in range : 1x, 3x (default), 6x, 9x, 18x
        * @param val gain value - COLOR_14_CLICK_LS_GAIN_1X
        */
        void setGainRGB(int val);

        /**
        * @brief Read the red data from the Color_14_Click module
        * @details Read the red data from the Color_14_Click module
        *   and update the member value of the object - 
        *
        * @return the Red component of the light.
        */
        int readRedValue(void);

        /**
        * @brief Read the green data from the Color_14_Click module
        * @details Read the green data from the Color_14_Click module
        *   and update the member value of the object - 
        *
        * @return the Green component of the light.
        */
        int readGreenValue(void);

        /**
        * @brief Read the blue data from the Color_14_Click module
        * @details Read the blue data from the Color_14_Click module
        *   and update the member value of the object - 
        *
        * @return the Blue component of the light.
        */
        int readBlueValue(void);

        /**
        * @brief Read the InfraRed data from the Color_14_Click module
        * @details Read the infrared data from the Color_14_Click module
        *   and update the member value of the object - 
        *
        * @return the IR component of the light.
        */
        int readIRValue(void);

        /**
        * @brief Collect all the RGBIR data from the Color_14_Click module
        * @details Read all the RGBIR data from the Color_14_Click module
        *   and update the members value of the object - 
        *
        * @param rgbIR first cell of a 4 int arrays
        * @return R G B IR value in a 4 int arrays
        */
        void readRGBIRValue(int rgbIR[]);
};

#endif