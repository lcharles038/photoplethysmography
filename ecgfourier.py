import riffourier as rif
import numpy
import matplotlib.pyplot as plt
from numpy import genfromtxt
import scipy.signal

signal = genfromtxt('data/out6_1.csv', delimiter=',')/1024*5
sig = genfromtxt('data/out6_0.csv', delimiter=',')/1024*5-1.14

fe=200
a=0.8/fe
b=3.5/fe
P=200
te=1/fe
t = numpy.arange(start=0.0,stop=len(signal)*te,step=te)


#h = h*scipy.signal.get_window("hamming",2*P+1)
h=rif.filtreRIF('PBande', a, b, P, fenetre="rect" )

'''
(f,g,phi)=rif.reponseFreq(h)
fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_xlabel('freq (Hz)')
ax1.set_ylabel('|H|', color=color)
ax1.plot(f*fe, g, color=color)
ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.set_ylabel('phi', color=color)  # we already handled the x-label with ax1
ax2.plot(f*fe, phi, color=color)
ax2.tick_params(axis='y', labelcolor=color)
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.xlim(0,5)
'''

y = 1.6+scipy.signal.convolve(signal*-60,h, mode='valid')
ny = y.size
ty = numpy.zeros(ny)
for k in range(ny):
    ty[k] = P*te+te*k   # P*te correspond au retard induit par le filtre
plt.figure(figsize=(10,4))
plt.plot(ty, y,'r', label="Signal filtré numériquement")
plt.plot(t,sig,'b', label="Signal filtré analogiquement")
plt.legend(loc='upper right')
plt.xlabel('t(s)')
plt.ylabel('U(V)')

'''indices = numpy.arange(2*P+1)
plt.figure(figsize=(8,4))
plt.vlines(indices,[0],h)
'''

plt.grid()
plt.show()
