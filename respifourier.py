import riffourier as rif
import numpy
import matplotlib.pyplot as plt
from numpy import genfromtxt
import scipy.signal

signal = genfromtxt('data/out6_1.csv', delimiter=',')/1024*5
fe=200
a=0.1/fe
b=0.3/fe
P=800
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
plt.xlim(0,0.5)

'''

y = scipy.signal.convolve(signal,h, mode='valid')
ny = y.size
ty = numpy.zeros(ny)
for k in range(ny):
    ty[k] = P*te+te*k   # P*te correspond au retard induit par le filtre
plt.figure(figsize=(10,4))
plt.plot(ty[10*fe:55*fe], y[10*fe:55*fe],'g')
plt.xlabel('t(s)')
plt.ylabel('U(V)')



plt.grid()
plt.show()
