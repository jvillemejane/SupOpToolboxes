/**
 * FILENAME :        WS2812.h          
 *
 * DESCRIPTION :
 *       WS2812 / RGB Led.
 *
 *       WS2812 Leds are Intelligent control LED integrated light source.
 *       More informations : https://cdn-shop.adafruit.com/datasheets/WS2812.pdf
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    07/feb/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 *      Adapted from Brian Daniels Library : https://os.mbed.com/users/bridadan/code/WS2812_Example/
 */

#ifndef __WS2812_HEADER_H__
#define __WS2812_HEADER_H__

#include <mbed.h>
 
#define FRAME_SIZE 24

/**
 * @class WS2812
 * @brief Control WS2812 RGB Led
 * @details     WS2812 Leds are Intelligent control LED integrated light source.
 */
class WS2812
{
public:

    /**
    * @brief Simple constructor of the WS2812 class.
    *
    * @param led Output pin. Connect to "Din" on the first WS2812 in the strip
    * @param size Number of LEDs in the strip
    * @param zeroHigh How many NOPs to insert to ensure TOH is properly generated. See library description for more information.
    * @param zeroLow How many NOPs to insert to ensure TOL is properly generated. See library description for more information.
    * @param oneHigh How many NOPs to insert to ensure T1H is properly generated. See library description for more information.
    * @param oneLow How many NOPs to insert to ensure T1L is properly generated. See library description for more information.
    *
    */
    WS2812(DigitalOut *led, int size, int zeroHigh, int zeroLow, int oneHigh, int oneLow);

    /*!
    Destroys instance.
    */
    ~WS2812();
    
    /**
    *   Sets the timing parameters for the bit-banged signal
    *
    * @param zeroHigh How many NOPs to insert to ensure TOH is properly generated. See library description for more information.
    * @param zeroLow How many NOPs to insert to ensure TOL is properly generated. See library description for more information.
    * @param oneHigh How many NOPs to insert to ensure T1H is properly generated. See library description for more information.
    * @param oneLow How many NOPs to insert to ensure T1L is properly generated. See library description for more information.
    *
    */
    void setDelays(int zeroHigh, int zeroLow, int oneHigh, int oneLow);

    /**
    *   Writes the given buffer to the LED strip with the given offsets.
    *   NOTE: This function is timing critical, therefore interrupts are disabled during the transmission section.
    *
    * @param r_offset The offset where each each pixel pulls its red component. Wraps to beginning if end is reached.
    * @param g_offset The offset where each each pixel pulls its green component. Wraps to beginning if end is reached.
    * @param b_offset The offset where each each pixel pulls its blue component. Wraps to beginning if end is reached.
    *
    */
    void write_offsets(int r_offset = 0, int g_offset = 0, int b_offset = 0);


    /**
    *   Writes the given buffer to the LED strip
    *   NOTE: This function is timing critical, therefore interrupts are disabled during the transmission section.
    *
    */
    void write(void);
    
    /**
    *   Sets the brightness mode : same brightness for all the pixels or each pixel are independents
    *
    * @param gb Use the global brightness true or false
    *
    */
    void useGlobalBrightness(bool gb);
    
    /**
    *   Sets the global brightness level.
    *
    * @param GB The brightness level. Possible values include 0 - 255 (0x00 - 0xFF).
    *
    */
    void setGlobalBrightness(unsigned char GB);

     /**
    *   Gets the buffer of pixels
    *
    * @return Pointer to the buffer of pixels.
    *
    */   
    int* getBuf(void);
    

    void SetAll(unsigned int);
    void SetAllI(unsigned char);
    void SetAllR(unsigned char);
    void SetAllG(unsigned char);
    void SetAllB(unsigned char);

    // location, value
    void Set(int, unsigned int);
    void SetI(int, unsigned char);
    void SetR(int, unsigned char);
    void SetG(int, unsigned char);
    void SetB(int, unsigned char);


private:
    /// Array of pixels
    int     *__pBuf;
    /// Size of the strip
    int     __size;
    /// Timing value (in us) fot the bit-banged signal
    int     __zeroHigh, __zeroLow, __oneHigh, __oneLow;
    /// Global Brightness - 0 to 255
    unsigned char __GB;
    /// Use global brightness or not
    bool    __use_GB;
    ///
    bool    *__transmitBuf;
    ///
    void    __loadBuf(int r_offset=0, int g_offset=0, int b_offset=0);
    /// Digital output for the led strip
    DigitalOut *__led;

    
    void __set_pixel_component(int index, int channel, int value);
    void __set_pixel(int index, int value);
};



#endif