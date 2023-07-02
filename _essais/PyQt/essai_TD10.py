# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:50:35 2023

@author: Villou
"""


import numpy as np
import control as ct
from systemSimu import *
import matplotlib.pyplot as plt


phD = photodetection()

sysDemo = systemSimulation()

''' Simulation parameters '''
samplesT = 1001
sysDemo.setTimeParams(0, 1, samplesT)
samplesF = 1001
freqMax = higherPowerOfK(phD.AOP.getGBW(), 10) + 2
sysDemo.setFreqParams(0, freqMax, samplesF)
''' Data '''
timeData = np.zeros((samplesT, 2))
timeSignal = np.zeros((samplesT, 2))
freqData = np.zeros((samplesT, 2))
freqSignalM = np.zeros((samplesT, 2))

''' Data '''
aliTF = phD.AOP.transferFunction()
sysDemo.setModel(aliTF)
timeData[:,0], timeSignal[:,0] = sysDemo.timeResponse()
freqData[:,0], freqSignalM[:,0], freqSignalInitP = sysDemo.freqResponse()
sysTF = phD.transferFunctionSimple()
sysDemo.setModel(sysTF)
timeData[:,1], timeSignal[:,1] = sysDemo.timeResponse()
freqData[:,1], freqSignalM[:,1], freqSigP = sysDemo.freqResponse()

sysCompletTF = phD.transferFunction()
sysDemo.setModel(sysCompletTF)
timeData[:,1], timeSignal[:,1] = sysDemo.timeResponse()
freqData[:,1], freqSignalM[:,1], freqSigP = sysDemo.freqResponse()

plt.figure()
plt.plot(timeData[:,0], timeSignal[:,0])
plt.plot(timeData[:,1], timeSignal[:,1])

plt.figure()
plt.plot(freqData[:,0], 20*np.log10(freqSignalM[:,0]))
plt.plot(freqData[:,1], 20*np.log10(freqSignalM[:,1]))
plt.xscale('log')


'''
RT = 1e6;           # resistance de contre-reaction
Cphd = 70e-12;      # capacité de la photodiode
wc = 1/(RT*Cphd);   # pulsation de coupure RT Cphd
fc = wc/(2*np.pi)

f = np.logspace(0,9,10001);
w = 2*np.pi*f;

## Ampli Opérationnel / ALI
# Modèle de l'ALI
A0 = 1e5;               # Amplification différentielle A
funitaire = 1e6;        # Bande-passante unitaire
f0 = funitaire/A0       # Fréquence de coupure en boucle ouverte
w0 = 2*np.pi*f0;

# Modèle premier ordre
num_AOP = [A0];
den_AOP = [1/w0, 1];
TF_AOP = ct.TransferFunction(num_AOP, den_AOP)
#mag, phase, omega = ct.bode(TF_AOP, w)


## Contre-réaction avec RT
num_moins = [1];
den_moins = [1/wc, 1];
TF_moins = ct.TransferFunction(num_moins, den_moins)
#                  mag_moins, phase_moins, w_moins = ct.bode(TF_moins, w);


## Action avec iphd
num_plus = [RT];
den_plus = [1/wc, 1];
TF_plus = ct.TransferFunction(num_plus, den_plus)
mag_plus, phase_plus, w_plus = ct.bode(TF_plus, w);

## Système rebouclé
TF_Vphd = ct.feedback(TF_AOP, TF_moins, -1);
mag_Vphd, phase_Vphd, w_Vphd = ct.bode(TF_Vphd, w);


## Système complet
TF_Iphd = TF_plus*TF_Vphd;
mag_Iphd, phase_Iphd, w_Iphd = ct.bode(TF_Iphd, w);


%% Modèle équivalent simplifié
wc
wu = funitaire*2*pi
wtrans = sqrt(wc*2*pi*funitaire)
Qtrans = sqrt(funitaire/fc)
num_trans = [RT*A0/(1+A0)];
den_trans = [1/(wtrans*wtrans) 1/(wtrans*Qtrans) 1];
TF_trans = tf(num_trans, den_trans)
[mag_trans, phase_trans, w_Iphd] = bode(TF_trans, w);
mag_trans = squeeze(mag_trans); phase_trans = squeeze(phase_trans);

% Diagramme de Bode / Comparaison
figure;
subplot(2,1,1); semilogx(f, 20*log10(abs(mag_trans)), f, 20*log10(abs(mag_Iphd)));
grid on; title('Réponse en fréquence du transimpédance - modele'); 
xlabel('fréquence (Hz)'); ylabel('Gain (dB) / Trans M');
legend('Modele','Transimpedance');
subplot(2,1,2); semilogx(f, phase_trans, f, phase_Iphd);
grid on; xlabel('fréquence (Hz)'); ylabel('Phase (deg)');

'''