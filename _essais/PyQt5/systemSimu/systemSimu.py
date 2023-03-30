# -*- coding: utf-8 -*-
"""
Signal Processing libraries of functions

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Version : 1.0 - 2022-12-01
"""

import numpy as np
import control as ct

'''
Find the power of K just higher than N
'''
def higherPowerOfK(N, K):
    # Finding log of the element
    lg = int(np.log(N) / np.log(K))
    return lg + 1


'''Photodetection class'''
class photodetection():
    
    def __init__(self):
        self.RT = 1e6           # resistance de contre-reaction
        self.Cphd = 70e-12      # capacité de la photodiode
        self.Re = 1e6           # Resistance entree oscilloscope
        self.Ce = 120e-12       # Capacite Cables
        self.wc = 1/(self.RT*self.Cphd);   # pulsation de coupure RT Cphd
        self.AOP = compALI(1e5, 3e6)
    
    def transferFunctionSimple(self):
        ''' System Model - require control library '''
        self.req = self.RT * self.Re / (self.RT + self.Re)
        self.ceq = self.Ce + self.Cphd
        self.transferFuncS = ct.tf([self.req],[(self.req * self.ceq), 1])
        return self.transferFuncS
    
    def transferFunctionFeedback(self):
        num_moins = [1];
        den_moins = [1/self.wc, 1];
        self.transferFuncF = ct.TransferFunction(num_moins, den_moins)
        return self.transferFuncF
 
    def transferFunction(self):
        TF_moins = self.transferFunctionFeedback()
        
        ## Action avec iphd
        num_plus = [self.RT];
        den_plus = [1/self.wc, 1];
        TF_plus = ct.TransferFunction(num_plus, den_plus)

        ## Système rebouclé
        TF_AOP = self.AOP.transferFunction()
        TF_Vphd = ct.feedback(TF_AOP, TF_moins, -1);


        ## Système complet
        TF_Iphd = TF_plus*TF_Vphd;
        
        return TF_Iphd 
 
    def setRt(self, rt):
        self.RT = rt        
        self.wc = 1/(self.RT*self.Cphd);   # pulsation de coupure RT Cphd
 
    def setCphd(self, cphd):
        self.Cphd = cphd        
        self.wc = 1/(self.RT*self.Cphd);   # pulsation de coupure RT Cphd
       
    def setCe(self, Ce):
        self.Ce = Ce    
        
    def setRe(self, re):
        self.Re = re    
    


'''
ALI class - component model
'''
class compALI():
    def __init__(self, gain=1e5, gbw=3e6):
        self.gain = gain
        self.gbw = gbw
        self.cutPuls = 2*np.pi*(self.gbw / self.gain)  
    
    def transferFunction(self):
        ''' System Model - require control library '''
        self.transferFunc = ct.tf([self.gain],[1/self.cutPuls, 1])
        return self.transferFunc
    
    def setGain(self, gain):
        self.gain = gain
        self.cutPuls = 2*np.pi*(self.gbw / self.gain)  
        
    def setGBW(self, gbw):
        self.gbw = gbw
        self.cutPuls = 2*np.pi*(self.gbw / self.gain)
    
    def getGBW(self):
        return self.gbw
    
    def getGain(self):
        return self.gain

'''
firstOrderSystem class - component model
'''
class firstOrderSystem():
    def __init__(self, type='LP', gain=1, fc=1e3):
        '''
        First Order System constructor, with
        Gain and cut frequency as parameter.
        Type of response is setable as low pass, high pass or derivative
        or integration function.

        Parameters
        ----------
        type : str, optional
            Type of the response : 
                - LP : low pass
                - HP : high pass
                - IN : integration
                - DR : derivative
            The default is 'LP'.
        gain : TYPE, optional
            DESCRIPTION. The default is 1.
        fc : TYPE, optional
            DESCRIPTION. The default is 1e3.

        Returns
        -------
        None.

        '''
        self.type = type
        self.gain = gain
        self.fc = fc
        self.cutPuls = 2*np.pi*(self.fc)  
    
    def transferFunction(self):
        ''' System Model - require control library '''
        if(self.type == 'LP'):
            self.transferFunc = ct.tf([self.gain],[1/self.cutPuls, 1])
        elif(self.type == 'HP'):
            self.transferFunc = self.gain * ct.tf([1/self.cutPuls, 1], [1])
        elif(self.type == 'DR'):
            self.transferFunc = self.gain * ct.tf([1/self.cutPuls, 0], [1])
        elif(self.type == 'IN'):
                self.transferFunc = ct.tf([self.gain],[1/self.cutPuls, 0])
        return self.transferFunc
    
    def setGain(self, gain):
        self.gain = gain 
        
    def setCutFreq(self, fc):
        self.fc = fc
        self.cutPuls = 2*np.pi*(self.fc)
    
    def getCutFreq(self):
        return self.fc
    
    def getGain(self):
        return self.gain

'''
SystemSimulation class
'''
class systemSimulation():
    def __init__(self):
        self.minTime = 0
        self.maxTime = 1
        self.samplesT = 101
        self.minFreq = 1
        self.maxFreq = 1e4
        self.samplesF = 101
        
    def setModel(self, transferFunc):
        self.transferFunc = transferFunc

    def setTimeParams(self, minT, maxT, samples):
        '''
        

        Parameters
        ----------
        minT : float
            minimal time value for simulation - in seconds.
        maxT : float
            maximal time value for simulation - in seconds.
        samples : int
            number of samples to generate for time simulation

        Returns
        -------
        None.

        '''        
        self.minTime = minT
        self.maxTime = maxT
        self.samplesT = samples

    def setFreqParams(self, minF, maxF, samples):
        '''
        

        Parameters
        ----------
        minF : float
            minimal frequency value for simulation - in Hz.
        maxF : float
            maximal frequency value for simulation - in Hz.
        samples : int
            number of samples to generate for frequency simulation

        Returns
        -------
        None.

        '''        
        self.minFreq = minF
        self.maxFreq = maxF
        self.samplesF = samples
        
    def timeResponse(self):
        timeV = np.linspace(self.minTime, self.maxTime, self.samplesT)
        if(self.transferFunc):
            T, yout = ct.step_response(self.transferFunc, timeV)
            return T, yout
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"No transfer Function is set")
            msg.setWindowTitle("No transfer Function")
            msg.exec_()

    def freqResponse(self):
        freqV = np.logspace(self.minFreq, self.maxFreq, self.samplesF)
        if(self.transferFunc):
            mag, phase, omega = ct.bode(self.transferFunc, freqV, plot=False, deg=True)
            return omega, mag, phase
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText(f"No transfer Function is set")
            msg.setWindowTitle("No transfer Function")
            msg.exec_()


if __name__ == '__main__':
    print("Control system - LEnsE")
    print("requires control library (PyPi)")