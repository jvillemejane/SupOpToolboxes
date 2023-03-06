import pygame
import numpy as np

class HarpeSound:
    
    sampleTimeSec = 3
    samplerate = 44100
    sampleMaxvalue = int(sampleTimeSec*samplerate)
        
    def __init__(self):               
        pygame.mixer.init(frequency=44100, channels=2, size=32)
        
        self.soundA4 = self.openWaveFile('A4.wav')
        self.soundA0 = self.generateSine(50,3)  # !! erreur sur la frequence...
        self.soundA1 = self.generateSine(100,3)  # !! erreur sur la frequence...
        
        self.soundA2 = (self.soundA4 + self.soundA0 + self.soundA1)
        
        
    def generateSine(self, frequency, duration):
        time = np.arange(0, duration, 1/HarpeSound.samplerate)
        dataR = np.sin(2*np.pi*frequency*time).astype(np.float32)
        data = np.array([dataR, dataR])
        sound = pygame.mixer.Sound(data)
        raw = sound.get_raw()
        bytes_array = np.frombuffer(raw, dtype=np.uint8)
        float_array = bytes_array.view(dtype=np.float32)
        return float_array[0:HarpeSound.sampleMaxvalue]
        
        
    def openWaveFile(self, file):
        sound = pygame.mixer.Sound(file)
        raw = sound.get_raw()
        bytes_array = np.frombuffer(raw, dtype=np.uint8)
        float_array = bytes_array.view(dtype=np.float32)
        return float_array[0:HarpeSound.sampleMaxvalue]

    
    def jouer_note (self,list,e):
        self.sound_creatorA4()
    
    
    def sound_creatorA2 (self):        
        pygame.mixer.Sound(self.soundA2[0:HarpeSound.sampleMaxvalue]).play(0)
    def sound_creatorA4 (self):        
        pygame.mixer.Sound(self.soundA4[0:HarpeSound.sampleMaxvalue]).play(0)

  
    
    
if __name__ == "__main__":
    controleur = HarpeSound()
    controleur.sound_creatorA2()
