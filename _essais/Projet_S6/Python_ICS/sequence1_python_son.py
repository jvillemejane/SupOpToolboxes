import pandas
import numpy as np
import matplotlib.pyplot as plt

# Lecture avec Pandas
df = pandas.read_csv('mus_mod.txt', header=0)
# print(df)
sampling_time = df.Time[1]-df.Time[0] # temps d'echantillonnage
sampling_rate = 1/sampling_time       # frequence d'echantillonnage
t = df.Time    # vecteur temps

# FFT
XVolt = np.fft.fft(df['Volt'])
N = len(XVolt)
#   vecteur freq
freq = np.linspace(-sampling_rate/2, sampling_rate/2-sampling_rate/N, N)
#   affichage FFT
plt.figure(figsize = (12, 6))
plt.plot(freq, np.fft.fftshift(np.abs(XVolt)/N))
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Signal porteuse
t = df.Time
#   demande a l'utilisateur la valeur de la frequence de la porteuse (selon FFT)
freq_p = float(input('Frequence de la porteuse (Hz) ? '))
x = np.sin(2*np.pi*freq_p*t)

# Demodulation
x_dem = x * df.Volt
XVoltDem = np.fft.fft(x_dem)
plt.figure(figsize = (12, 6))
plt.plot(freq, np.fft.fftshift(np.abs(XVoltDem)/N))
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Filtrage
fmin = 1-freq_p/sampling_rate # freq normalisee + shift fft
fmax = freq_p/sampling_rate
nfe2 = int(np.ceil(N/2))
nmax = int(np.ceil(fmax * N))
nmin = int(np.ceil(fmin * N))
print('Fe/2 = '+ str(nfe2) + ' // Nmax = '+ str(nmax))

for k in range (nmax,nfe2) :
    XVoltDem[k] = 0.0
for k in range (nfe2, nmin) :
    XVoltDem[k] = 0.0
plt.figure(figsize = (12, 6))
plt.plot(freq, np.fft.fftshift(np.abs(XVoltDem)/N))
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude')
plt.show()

# Reconstruction signal
xdem = np.fft.ifft(XVoltDem)
plt.plot(t, np.abs(xdem))
plt.xlabel('Temps (s)')
plt.ylabel('Amplitude (V)')
plt.show()


# sound
import sounddevice as sd
print(int(sampling_rate))
# sd.play(xdem.real, int(sampling_rate))

import wave
obj = wave.open('sound.wav','w')
obj.setnchannels(1) # mono
obj.setsampwidth(2)
obj.setnframes(N)
obj.setframerate(int(sampling_rate))
for i in range(N):
   data = xdem[i].real*64000
   obj.writeframesraw( data )
obj.close()
