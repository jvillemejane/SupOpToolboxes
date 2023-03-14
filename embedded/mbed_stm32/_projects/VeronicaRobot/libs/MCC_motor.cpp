/**
 * FILENAME :        MCC_motor.cpp          
 *
 * DESCRIPTION :
 *       Direct Current Motor control library (with Half-Bridge).
 **
 * AUTHOR :    Julien VILLEMEJANE        START DATE :    13/mar/2023
 *
 *       LEnsE / Institut d'Optique Graduate School
 */

 #include   "MCC_motor.h"

MCC_motor::MCC_motor(PwmOut *D1, PwmOut *D2){
    this->_enable = false;
    this->_enGlobal = false;
    this->_coder = false;
    this->_period_us = 500;

    if (D1){ delete this->_D1; }
    this->_D1 = D1;
    this->_D1->period_us(this->_period_us);
    this->_D1->write(0);
    if (D2){ delete this->_D2; }
    this->_D2 = D2;
    this->_D2->period_us(this->_period_us);
    this->_D2->write(0);
}


void MCC_motor::setEnablePin(DigitalOut *en, bool global){
    if (en){ delete this->_en; }
        this->_en = en;  
    this->_enGlobal = global;  
}

void MCC_motor::setEnable(void){
    this->_enable = true;
    this->_en->write(1);
}

void MCC_motor::setDisable(void){
    this->_enable = false;
    this->_en->write(0);
}

bool MCC_motor::isEnabled(void){
    return this->_enable;
}


void MCC_motor::setPwmPeriod_us(int per_us){
    this->_period_us = per_us;
    this->_D1->period_us(this->_period_us);
    this->_D2->period_us(this->_period_us);
}


void MCC_motor::stop(void){
    if(!this->_enGlobal){
        this->_en->write(0);
    }
    this->_D1->write(0);
    this->_D2->write(0);
}    

void MCC_motor::goForward(float rel_speed){
    this->_rc = rel_speed;
    if(!this->_enGlobal){
        this->_en->write(1);
    }
    this->_D1->write(this->_rc);
    this->_D2->write(0);
}


void MCC_motor::goBackward(float rel_speed){
    this->_rc = rel_speed;
    if(!this->_enGlobal){
        this->_en->write(1);
    }
    this->_D1->write(0);
    this->_D2->write(this->_rc);
}

bool MCC_motor::rotate(float rel_speed){
    if(rel_speed > 0){
        this->goForward(rel_speed);
        return true;
    }
    else{
        if(rel_speed < 0){
            this->goBackward(-rel_speed);
            return false;
        }
        else{
            this->stop();
            return false;
        }
    }
}

void MCC_motor::setCoderPin(InterruptIn *cA, InterruptIn *cB, bool inc){
    if (cA){ delete this->_cA; }
        this->_cA = cA; 
    if (cB){ delete this->_cB; }
        this->_cB = cB; 
    this->_cnt_coder = 0;
    this->_inc_cnt = inc;
    // 4 states per count
    this->_cA->rise(callback(this, &MCC_motor::ISR_coder_counter));
    this->_cA->fall(callback(this, &MCC_motor::ISR_coder_counter));
    this->_cB->rise(callback(this, &MCC_motor::ISR_coder_counter));
    this->_cB->fall(callback(this, &MCC_motor::ISR_coder_counter));
}

int MCC_motor::getCoderCnt(void){
    return this->_cnt_coder;
}

void MCC_motor::ISR_coder_counter(void){
    // state detection of CPR encoder - https://www.cuidevices.com/blog/what-is-encoder-ppr-cpr-and-lpr#cpr
    this->_coder_new_state = (this->_cB->read() << 1) + this->_cA->read();
    if(this->_coder_anticlockwise[this->_coder_old_state] == this->_coder_new_state){
        this->_cnt_coder--;
    }
    else{
        if(this->_coder_clockwise[this->_coder_old_state] == this->_coder_new_state){
            this->_cnt_coder++;
        }
    }
    this->_coder_old_state = this->_coder_new_state;    
}