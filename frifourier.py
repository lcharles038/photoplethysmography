import numpy
import math
from matplotlib.pyplot import *
from numpy import genfromtxt
import scipy.signal

voie1 = genfromtxt('data/out6_1.csv', delimiter=',')/1024*5
#signal=voie1[::4]
signal=voie1
fe=200
#respi
a=0.1/fe
b=0.3/fe
P=800
#coeur
#a=1/fe
#b=3.5/fe
#P=100
te=1/fe
t = numpy.arange(start=0.0,stop=len(signal)*te,step=te)
h = numpy.zeros(2*P+1)


def filtreRIFgeneral(g,P,fenetre):
    N=2*P+1 # ordre du filtre
    liste_k = numpy.arange(start=-P,stop=P+1)
    n = liste_k.size
    h = numpy.zeros(n)
    for k in range(n):
        h[k] = g(liste_k[k])
    if fenetre!="rect":
        h = h*scipy.signal.get_window(fenetre,N)
    print (h)
    return h

def filtreRIF(type,a=0.5,b=0,P=50,fenetre="rect"):
    print (b)
    if type=='PBas':
        def g(k):
            return 2*a*numpy.sinc(k*2*a)
    elif type=='PHaut':
        def g(k):
            if k==0:
                return 1-2*b
            else:
                return -2*b*numpy.sinc(k*2*b)
    elif type=='PBande':
        def g(k):
            if k==0:
                return 2*(b-a)
            else:
                return (numpy.sin(2*math.pi*k*b)-numpy.sin(2*math.pi*k*a))/(k*math.pi)
    elif type=='CBande':
        def g(k):
            if k==0:
                return 2*(a-b)+1
            else:
                return (numpy.sin(2*math.pi*k*a)-numpy.sin(2*math.pi*k*b))/(k*math.pi)
    else:
        def g(k):
            return 1.0
    return filtreRIFgeneral(g,P,fenetre)

def reponseFreq(h):
    N = h.size
    def Hf(f):
        s = 0.0
        for k in range(N):
            s += h[k]*numpy.exp(-1j*2*math.pi*k*f)
        return s
    f = numpy.arange(start=0.0,stop=0.5,step=0.0001)
    hf = Hf(f)
    g = numpy.absolute(hf)
    phi = numpy.unwrap(numpy.angle(hf))
    return [f,g,phi]



#Reponse impulsionnelle du filtre
'''h=filtreRIF('PBande', a, b, P=P, fenetre="rect" )
h = h*scipy.signal.get_window("hamming",2*P+1)
indices = numpy.arange(2*P+1)
figure(figsize=(8,4))
vlines(indices,[0],h)
grid()
show()'''



#Reponse fréquentielle du filtre
'''
h=filtreRIF('PBande', a, b, P=P, fenetre="rect" )
h = h*scipy.signal.get_window("hamming",2*P+1)
(f,g,phi)=reponseFreq(h)
fig, ax1 = subplots()
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
xlim(0,0.5)

grid()
show()
'''


h=filtreRIF('PBande', a, b, P, fenetre="rect" )
# ECG
#y = -68*scipy.signal.convolve(signal,h,mode='valid') + 5
#Respi
y = -scipy.signal.convolve(signal,h, mode='valid')

##h=filtreRIF('PBande', a=0.75/fe, b=3/fe, P=150, fenetre="rect")
#y = -10*scipy.signal.convolve(signal,h,mode='valid')+1.14
ny = y.size
ty = numpy.zeros(ny)
for k in range(ny):
    ty[k] = P*te+te*k   # P*te correspond au retard induit par le filtre
figure(figsize=(10,4))

#plot(t,signal,'b')  #signal original
plot(ty, y,'r')
xlabel('t')
ylabel('y')
#axis([0,100])
grid()
show()


