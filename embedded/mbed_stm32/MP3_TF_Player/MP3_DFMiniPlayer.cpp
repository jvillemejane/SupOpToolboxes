/**
 * FILENAME :        MP3_DFMiniPlayer.cpp          
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
 */

#include "MP3_DFMiniPlayer.h"
#include <cstdint>

MP3_DFMiniPlayer::MP3_DFMiniPlayer(UnbufferedSerial *link){
    this->_receivedIndex = 0;
    this->_dataIsReady = false;
    this->_dataCnt = 0;
    this->_playerReady = false;

    /* Initialisation of enable output */
    if (link){ delete this->_serial; }
    this->_serial = link;
    this->_serial->baud(9600);      // 9600 bauds default value
    this->_serial->attach(callback(this, &MP3_DFMiniPlayer::ISR_MP3_data), UnbufferedSerial::RxIrq);

    /* Initialization of the sending buffer */
    this->_sendingBuffer[0] = START_BYTE;
    this->_sendingBuffer[1] = VERSION_BYTE;
    this->_sendingBuffer[2] = LENGTH_BYTE;
    this->_sendingBuffer[9] = END_BYTE;

}

void MP3_DFMiniPlayer::ISR_MP3_data(void){
    uint8_t data = 0;
    this->_serial->read(&data, 1);

    // echo mode - DEBUG
    this->_debug->write(&data, 1);

    if(data == START_BYTE){ this->_receivedIndex = 0;   }
    else{   this->_receivedIndex++; }
    this->_receivedBuffer[this->_receivedIndex] = data;
    if((data == END_BYTE) && (this->_receivedIndex == 9)){
        this->_dataIsReady = true;
        this->_dataCnt++;
    }
}

uint16_t    MP3_DFMiniPlayer::calculateCheckSum(uint8_t *buffer){
    uint16_t sum = 0;
    for (int i = START_CHKSUM; i <=  END_CHKSUM; i++) {
        sum += buffer[i];
    }
    return -sum;
}


bool        MP3_DFMiniPlayer::checkCheckSum(uint8_t *buffer){
    uint16_t chS = calculateCheckSum(buffer);
    uint16_t chSR = (buffer[7] << 8) + buffer[8];
    return (chS == chSR);
}


/*
* @return  1 if USB, 2 if SD Card, 3 if both, 4 if computer
*/
int8_t    MP3_DFMiniPlayer::waitAvailable(void){
    if((this->_dataIsReady) && (this->_dataCnt == 1)){
        if(checkCheckSum(this->_receivedBuffer)){
            if(this->_receivedBuffer[3] == QUERY_ONLINE){
                this->_playerReady = true;
                return this->_receivedBuffer[6];
            }
            else{
                return -1;
            }
        }
        return -2;
    }
    return -3;
}


void 	MP3_DFMiniPlayer::reset(void){
    // Specify playback of track 100 in the folder 11 // 7E FF 06 0F 00 0B 64 xx xx EF
    this->_sendingBuffer[3] = CMD_RESET;
    this->_sendingBuffer[4] = 0;
    this->_sendingBuffer[5] = 0;
    this->_sendingBuffer[6] = 0;
    uint16_t chSum = this->calculateCheckSum(this->_sendingBuffer);
    this->_sendingBuffer[7] = (chSum >> 8) & 0xFF;
    this->_sendingBuffer[8] = chSum & 0xFF;
    this->_serial->write(this->_sendingBuffer, BUFFER_SIZE);
}

void 	MP3_DFMiniPlayer::playTrack(uint16_t track, uint16_t dir){
    // Specify playback of track 100 in the folder 11 // 7E FF 06 0F 00 0B 64 xx xx EF
    this->_sendingBuffer[3] = CMD_PLAY_TR_DIR;
    this->_sendingBuffer[4] = 0;
    this->_sendingBuffer[5] = dir & 0xFF;
    this->_sendingBuffer[6] = track & 0xFF;
    uint16_t chSum = this->calculateCheckSum(this->_sendingBuffer);
    this->_sendingBuffer[7] = (chSum >> 8) & 0xFF;
    this->_sendingBuffer[8] = chSum & 0xFF;
    this->_serial->write(this->_sendingBuffer, BUFFER_SIZE);
}


void    MP3_DFMiniPlayer::playCmd(void){
    this->_sendingBuffer[3] = CMD_PLAY;
    this->_sendingBuffer[4] = 0;
    this->_sendingBuffer[5] = 0;
    this->_sendingBuffer[6] = 0;
    uint16_t chSum = this->calculateCheckSum(this->_sendingBuffer);
    this->_sendingBuffer[7] = (chSum >> 8) & 0xFF;
    this->_sendingBuffer[8] = chSum & 0xFF;
    this->_serial->write(this->_sendingBuffer, BUFFER_SIZE);
}


void    MP3_DFMiniPlayer::pauseCmd(void){
    this->_sendingBuffer[3] = CMD_PAUSE;
    this->_sendingBuffer[4] = 0;
    this->_sendingBuffer[5] = 0;
    this->_sendingBuffer[6] = 0;
    uint16_t chSum = this->calculateCheckSum(this->_sendingBuffer);
    this->_sendingBuffer[7] = (chSum >> 8) & 0xFF;
    this->_sendingBuffer[8] = chSum & 0xFF;
    this->_serial->write(this->_sendingBuffer, BUFFER_SIZE);
}


/// DEBUGGING SECTION

void    MP3_DFMiniPlayer::setDebugSerial(UnbufferedSerial *debug){
    if (debug){ delete this->_debug; }
        this->_debug = debug;
    this->_debug->baud(115200);
    sprintf(this->chStr, "DEBUG MODE\n");
	this->_debug->write(this->chStr, strlen(this->chStr));
}

int     MP3_DFMiniPlayer::getDataCnt(void){
    return this->_dataCnt;
}