import numpy as np
import matplotlib.pyplot as plt

## Paramètres échantillonnage
Fe = 1e3
Npoints = 1001
T = Npoints/Fe

## Signaux
# vecteur temps
t = np.linspace(0,T,Npoints)
# vecteur signal
v = np.sin(2*np.pi*400*t)

## affichage
plt.figure()
plt.title('Sinus 400 Hz')
plt.xlabel('Temps (s)')
plt.ylabel('Amplitude (V)')
plt.plot(t, v)
plt.show()

## FFT
# Calcul TFd
TFv = np.fft.fft(v)
# Affichage "brut"
plt.figure()
plt.plot(np.absolute(TFv))
plt.show()

# Affichage "physicien"

freq = np.linspace(-Fe/2+Fe/(2*Npoints), Fe/2-Fe/(2*Npoints), Npoints)
plt.figure()
plt.plot(freq, np.fft.fftshift(np.absolute(TFv))/Npoints)
plt.title('Spectre d\'un signal sinusoidal')
plt.xlabel('Frequence (Hz)')
plt.ylabel('Amplitude (V)')
plt.show()

