/****************************************************************************/
/*  DMX_MIDI module library                                                 */
/****************************************************************************/
/*  LEnsE / Julien VILLEMEJANE       /   Institut d'Optique Graduate School */
/****************************************************************************/
/*  Library - DMX_MIDI.cpp file                                             */
/****************************************************************************/
/*  Tested on Nucleo-L476RG / 11th nov 2021                                 */
/****************************************************************************/

#include "DMX_MIDI.h"

/* Entrées - Sorties */
// DMX
Serial      dmx(PA_0, PA_1);
DigitalOut  out_tx(D5);
DigitalOut  start(D4);     //envoie des données
DigitalOut  enableDMX(D6);
// MIDI
Serial      midi(D8, D2);
// Analogiques
AnalogIn    CV_volume(PC_1);
AnalogIn    CV_pitch(PB_0);
AnalogIn    variationR(PC_0);
AnalogIn    variationG(PC_2);
AnalogIn    variationB(PC_3);

/* Variables globales */
char        dmx_data[SAMPLES] = {0};
int         rgb;
// Midi
char        cpt_midi;
char        new_data_midi, new_note_midi, midi_channel;
char        midi_data[3], note_data, velocity_data;
char        control_ch, control_value;

/* Fonction d'initialisation de la liaison DMX */
void initDMX(void){
    dmx.baud(250000);
    dmx.format (8, SerialBase::None, 2);
    enableDMX = 0;
    // Initialisation canaux DMX
    for(int k = 0; k < SAMPLES; k++){
        dmx_data[k] = 0;
    }    
    updateDMX();
} 

/* Fonction de mise à jour de la sortie DMX */
void updateDMX(){
        enableDMX = 1;
        start = 1;      // /start
        out_tx = 0;     // break
        wait_us(88);    
        out_tx = 1;     // mb
        wait_us(8);     
        out_tx = 0;     // break
        start = 0;
        dmx.putc(0);     // Start
        for(int i = 0; i < SAMPLES; i++){
            dmx.putc(dmx_data[i]);     // data
        }
        wait_us(23000); // time between frame  
}

/* Fonction d'initialisation de la liaison MIDI */
void initMIDI(void){
    midi.baud(31250);
    midi.format(8, SerialBase::None, 1);
    midi.attach(&ISR_midi_in, Serial::RxIrq);
}
/* Detection d'une note reçue en MIDI */
bool isNoteMIDIdetected(void){
    if(new_note_midi == 1)
        return true;
    else
        return false;
}
/* Note reçue en MIDI traitée */
void resetNoteMIDI(void){
    new_note_midi = 0;
}

/* Detection d'un controle reçu en MIDI */
bool isCCMIDIdetected(void){
    if(new_data_midi == 1)
        return true;
    else
        return false;
}
/* Controle reçu en MIDI traité */
void resetCCMIDI(void){
    new_data_midi = 0;
}

/* Renvoie la note reçue sur la liaison MIDI */
void resendNoteMIDI(void){
    midi.putc(MIDI_NOTE_ON);
    midi.putc(note_data);
    midi.putc(127);
}

/* Joue une note sur la liaison MIDI */
void playNoteMIDI(char note, char velocity){
    midi.putc(MIDI_NOTE_ON);
    midi.putc(note);
    midi.putc(velocity);
}

/* Stoppe une note sur la liaison MIDI */
void stopNoteMIDI(char note, char velocity){
    midi.putc(MIDI_NOTE_OFF);
    midi.putc(note);
    midi.putc(velocity);
}

/* Fonction d'interruption sur MIDI */
/* Format MIDI : 
		- 1 octet pour le type de message
		- 1 ou 2 octets pour l'information transmise (Note et Velocité, par exemple)
 */
void ISR_midi_in(void){
    debug_out = !debug_out;
	// Récupération de la donnée sur la liaison série
    char data = midi.getc();
	// Détection du premier octet (valeur > 128 d'après le protocole MIDI)
    if(data >= 128)
        cpt_midi = 0;
    else
        cpt_midi++;
	// Stocktage de la donnée reçue dans une des 3 cases du tableau midi_data
    midi_data[cpt_midi] = data;
	
	uint8_t message_type = midi_data[0] & 0xF0;
	midi_channel = midi_data[0] & 0x0F;
	
    if(cpt_midi == 2){
        cpt_midi = 0;
        if((message_type == MIDI_NOTE_ON) || (message_type == MIDI_NOTE_OFF)){
            new_note_midi = 1;
            note_data = midi_data[1];
            velocity_data = midi_data[2];
        }
        else{
            if(message_type == MIDI_CC){
                new_data_midi = 1;
                control_ch = midi_data[1];
                control_value = midi_data[2];
            }
        }
    }
}