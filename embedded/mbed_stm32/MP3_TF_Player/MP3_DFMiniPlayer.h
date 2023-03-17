/**
 * FILENAME :        MP3_DFMiniPlayer.h          
 *
 * DESCRIPTION :
 *       MP3 DF Mini Player module library.
 *
 * NOTES :
 *       Developped by Villou / LEnsE
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    16/mar/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 * @see https://github.com/DFRobot/DFRobotDFPlayerMini/blob/master/doc/FN-M16P%2BEmbedded%2BMP3%2BAudio%2BModule%2BDatasheet.pdf
 *
 *************************
 *      MP3 Commands : 
            $S          Start byte 0x7E
            Ver.        Version 0xFF by default
            Length      Number of byte from version info to Check_LSB, typically 0x06 (checksum not counted)
            CMD         Command Code
            Feedback    0x01: Need feedback--send confirmation back to MCU; 0x00: No need feedback
            Para_MSB    Most significant byte of parameter
            Para_LSB    Least significant byte of parameter
            Check_MSB   Most significant byte of checksum
            Check_LSB   Least significant byte of checksum
            $O          End byte 0xEF
        Trame Example : 7E FF 06 09 00 00 02 FF F0 EF  (play back on SD Card)

        Chechsum : (2 bytes) = 0xFFFF–(Ver.+Length+CMD+Feedback+Para_MSB+Para_LSB)+1
 */


#ifndef __MP3_DFMINIPLAYER_HEADER_H__
#define __MP3_DFMINIPLAYER_HEADER_H__

#include <cstdint>
#include <mbed.h>
 
/** Constant definition */
#define     DEBUG_MODE                  1

#define     BUFFER_SIZE     10
#define     START_CHKSUM    1
#define     END_CHKSUM      6 

#define     START_BYTE      0x7E
#define     VERSION_BYTE    0xFF
#define     END_BYTE        0xEF
#define     LENGTH_BYTE     0x06

#define     CMD_NEXT        0x01
#define     CMD_PREV        0x02
#define     CMD_INC_V       0x04
#define     CMD_DEC_V       0x05
#define     CMD_RESET       0x0C
#define     CMD_PLAY        0x0D
#define     CMD_PAUSE       0x0E
#define     CMD_PLAY_TR_DIR 0x0F
#define     QUERY_ONLINE    0x3F



/**
 * @class MP3_DFMiniPlayer
 * @brief Take control of a MP3 Player - DF Mini
 */
class MP3_DFMiniPlayer{
    private:
        UnbufferedSerial    *_serial;

        bool        _playerReady;

        uint8_t     _receivedBuffer[BUFFER_SIZE];
        uint8_t     _receivedIndex;
        bool        _dataIsReady;
        int         _dataCnt;

        uint8_t     _sendingBuffer[BUFFER_SIZE];

        uint16_t    calculateCheckSum(uint8_t *buffer);
        bool        checkCheckSum(uint8_t *buffer);


        UnbufferedSerial    *_debug;
        char        chStr[64];

    public:
        /**
        * @brief Simple constructor of the MP3_DFMiniPlayer class.
        * @param link USART link to the MP3 Player
        */
        MP3_DFMiniPlayer(UnbufferedSerial *link);

        /**
        * @brief Interrupt routine when data is received from the MP3 module
        */
        void ISR_MP3_data(void);

        /**
        * @brief Send the type of device connected after reset
        * @return  1 if USB, 2 if SD Card, 3 if both, 4 if computer
        */
        int8_t    waitAvailable(void);

        /**
        */
        void    reset(void);

        /**
        * @brief Play the indexed track in a specific directory
        * @param track number of the track
		* @param dir number of the directory (if 0, root directory)
        */		
		void 	playTrack(uint16_t track, uint16_t dir);

        /**
        * @brief Start playing a track
        */	
        void    playCmd(void);

        /**
        * @brief Pause a track
        */	
        void    pauseCmd(void);


        void    setDebugSerial(UnbufferedSerial *debug);
        int     getDataCnt(void);


};

#endif