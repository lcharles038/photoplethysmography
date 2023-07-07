import riffourier as rif
import numpy
import matplotlib.pyplot as plt
from numpy import genfromtxt
import scipy.signal

fe=200
b=10/fe
P=100
te=1/fe


#h = h*scipy.signal.get_window("hamming",2*P+1)
h=rif.filtreRIF('PBas', b, P=P, fenetre="rect" )


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
plt.xlim(0,20)

'''
#h = h*scipy.signal.get_window("hamming",2*P+1)
indices = numpy.arange(2*P+1)
print (len(h))
plt.figure(figsize=(8,4))
plt.vlines(indices,[0],h)
'''

plt.grid()
plt.show()
