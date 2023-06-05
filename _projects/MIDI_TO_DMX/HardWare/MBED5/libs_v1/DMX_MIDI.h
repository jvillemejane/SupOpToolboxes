/****************************************************************************/
/*  DMX_MIDI module library                                                 */
/****************************************************************************/
/*  LEnsE / Julien VILLEMEJANE       /   Institut d'Optique Graduate School */
/****************************************************************************/
/*  Library - DMX_MIDI.h file                                               */
/****************************************************************************/
/*  Tested on Nucleo-L476RG / 11th nov 2021                                 */
/****************************************************************************/

#ifndef     DMX_MIDI_H_INCLUDED
#define     DMX_MIDI_H_INCLUDED

#include    "mbed.h"

#define     SAMPLES     512 

#define     MIDI_NOTE_ON        0x90
#define     MIDI_NOTE_OFF       0x80
#define     MIDI_CC             0xB0

/* Entrées - Sorties */
extern      Serial      debug_pc;
extern      DigitalOut  debug_out;

extern      Serial      dmx;
extern      DigitalOut  out_tx;
extern      DigitalOut  start;     //envoie des données
extern      DigitalOut  enableDMX;
extern      AnalogIn    CV_volume;
extern      AnalogIn    CV_pitch;

extern      AnalogIn    variationR;
extern      AnalogIn    variationG;
extern      AnalogIn    variationB;

/* Variables globales */
extern      const uint8_t vague[];
extern      char        dmx_data[];
extern      int         rgb;
extern      char        cpt_midi;
extern      char        new_data_midi, new_note_midi;
extern      char        midi_data[], note_data, velocity_data;
extern      char        control_ch, control_value;

/* Fonctions */  
/* Fonction d'initialisation de la liaison DMX */
void initDMX(void);
/* Fonction de mise à jour de la sortie DMX */
void updateDMX();

/* Fonction d'initialisation de la liaison MIDI */
void initMIDI(void);
/* Fonction d'initialisation de la liaison MIDI - version beta */
void initMIDI2(void);
/* Detection d'une note reçue en MIDI */
bool isNoteMIDIdetected(void);
/* Note reçue en MIDI traitée */
void resetNoteMIDI(void);
/* Renvoie la note reçue sur la liaison MIDI */
void resendNoteMIDI(void);
/* Renvoie la note reçue sur la liaison MIDI - version beta */
void resendNoteMIDI2(void);
/* Joue une note sur la liaison MIDI */
void playNoteMIDI(char note, char velocity);
/* Joue une note sur la liaison MIDI - version beta */
void playNoteMIDI2(char note, char velocity);
/* Stoppe une note sur la liaison MIDI */
void stopNoteMIDI(char note, char velocity);

/* Detection d'un controle reçu en MIDI */
bool isCCMIDIdetected(void);
/* Controle reçu en MIDI traité */
void resetCCMIDI(void);

/* Fonction d'appel à une variation de lumière en fonction d'un angle
    @out : R G B au format 24 bits
*/
int sineLED(int angle);

/* Fonction d'interruption sur MIDI */
void ISR_midi_in(void);
/* Fonction d'interruption sur MIDI - version beta */
void ISR_midi_in2(void);

#endif