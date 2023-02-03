# -*- coding: utf-8 -*-
"""
Animation with Matplotlib

Author : Julien VILLEMEJANE
Laboratoire d Enseignement Experimental - Institut d Optique Graduate School
Created on Mon Jan 31 20:39:05 2023

@author: julien.villemejane
@see: https://courspython.com/animation-matplotlib.html
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

k = 2*np.pi
w = 2*np.pi
dt = 0.01

xmin = 0
xmax = 3
nbx = 151

x = np.linspace(xmin, xmax, nbx)

fig = plt.figure() # initialise la figure
line, = plt.plot([], []) 
plt.xlim(xmin, xmax)
plt.ylim(-1, 1)

def animate(i): 
    t = i * dt
    y = np.cos(k*x - w*t)
    line.set_data(x, y)
    return line,
 
anim = animation.FuncAnimation(fig, animate, frames=100,
                              interval=1, blit=True, repeat=False)
plt.show()


## Saving animation
# Gif format
f = r"animation.gif" 
writergif = animation.PillowWriter(fps=30) 
anim.save(f, writer=writergif)

# MP4 format - required ffmpeg
# ffmpeg installer from https://github.com/BtbN/FFmpeg-Builds/releases
import matplotlib as mpl 
mpl.rcParams['animation.ffmpeg_path'] = r'D:\\Logiciels\\ffmpeg\\bin\\ffmpeg.exe'

f = r"animation.mp4" 
writervideo = animation.FFMpegWriter(fps=60) 
anim.save(f, writer=writervideo)