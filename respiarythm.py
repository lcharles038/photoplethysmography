from scipy.signal import butter, lfilter, firwin
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz, find_peaks
from numpy import genfromtxt
import riffourier as rif
import scipy.signal


# Fréquence échantillonnage pour tous les signaux utilisés, en Hz.
signal = genfromtxt('data/out6_1.csv', delimiter=',')/1024*5

fe=200
te=1/fe

ac=0.8/fe
bc=3.5/fe
Pc=200
hc=rif.filtreRIF('PBande', ac, bc, Pc, fenetre="rect" )
ecg = 1.6+scipy.signal.convolve(signal*-60,hc, mode='valid')
nc = ecg.size
tc = np.zeros(nc)
for k in range(nc):
    tc[k] = Pc*te+te*k   # P*te correspond au retard induit par le filtre

ar=0.1/fe
br=0.3/fe
Pr=800
hr = rif.filtreRIF('PBande', ar, br, Pr, fenetre="rect" )
fr = scipy.signal.convolve(-signal,hr, mode='valid')
nr = fr.size
tr = np.zeros(nr)
for k in range(nr):
    tr[k] = Pr*te+te*k   # P*te correspond au retard induit par le filtre

peaks,_ = (find_peaks(ecg[10*fe:60*fe], distance=0.6*fe))
bpm=[]
for i in range (len(peaks)-1):
    bpm.append(60/(peaks[i+1]-peaks[i])*fe)
    # corrections
for i in range (len(bpm)-2):
    if (bpm[i+1] - bpm[i])>=10:
        bpm[i+1] = bpm[i]+0.33*(bpm[i+2]-bpm[i])
        bpm[i+2] = bpm[i]+0.66*(bpm[i+2]-bpm[i])
    if (bpm[i+1] - bpm[i])<=-10:
        bpm[i+1] = bpm[i]-0.33*(bpm[i]-bpm[i+2])
        bpm[i+2] = bpm[i]-0.66*(bpm[i]-bpm[i+2])

t = np.arange(start=0.0,stop=len(signal)*te,step=te)


plt.rcParams['axes.grid'] = True
fig, ( ax3, ax4, ax5) = plt.subplots(3, sharex=True)
ax3.plot(tc[10*fe:60*fe], (ecg)[10*fe:60*fe], 'red', label='Signal CG filtré numériquement')
ax3.plot((11 + peaks/fe), (ecg)[10*fe:60*fe][peaks],"x")
ax3.legend(loc='lower left')
ax3.set_ylabel('U(V)')
ax4.step((11+peaks[:-1]/fe), bpm, where='post', label='Fréquence cardiaque (bpm)')
ax4.legend(loc='upper right')
ax4.set_ylabel('FC(bpm)')
ax5.plot(tr[10*fe:55*fe], (fr)[10*fe:55*fe], 'green', label='Signal Respi filtré numériquement')
ax5.legend(loc='lower right')
ax5.set_ylabel('U(V)')
plt.xlabel('Temps (secondes)')
fig.suptitle('Deux recherches du signal respiratoire')
plt.grid(True)
plt.show()


