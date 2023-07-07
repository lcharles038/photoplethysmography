from math import cos, pi, sin
from matplotlib.pyplot import *
from scipy.signal import butter, lfilter, firwin
import scipy.signal
import numpy

def filtreRIFgeneral(g,P,fenetre):
    N=2*P+1 # ordre du filtre
    liste_k = numpy.arange(start=-P,stop=P+1)
    n = liste_k.size
    h = numpy.zeros(n)
    for k in range(n):
        h[k] = g(liste_k[k])
    if fenetre!="rect":
        h = h*scipy.signal.get_window(fenetre,N)
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
                return (numpy.sin(2*pi*k*b)-numpy.sin(2*pi*k*a))/(k*pi)
    elif type=='CBande':
        def g(k):
            if k==0:
                return 2*(a-b)+1
            else:
                return (numpy.sin(2*pi*k*a)-numpy.sin(2*pi*k*b))/(k*pi)
    else:
        def g(k):
            return 1.0
    return filtreRIFgeneral(g,P,fenetre)

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    print("a=")
    print (a)
    print("b=")
    print (b)
    y = lfilter(b, a, data)
    return y

def u(t):
    return (10*cos(2*pi*20*t + 3*sin(2*pi*5*t)))

def getSignal5(s):
    # Fréquence de coupure basse (volontairement très inférieure à celle du coeur afin de voir la respi...)
    fcBasse = 4.5
    fcHaute = 5.5
    r = butter_bandpass_filter(s, fcBasse, fcHaute, 1000, 3)
    return r

s=[]
t=[]
#te=0.001
te=0.005
fe = 1/te
P=200

for i in range (1000):
    s.append(u(i*te))
    t.append(i*te)

#figure(figsize=(6,4))
#plot(t,s)
#r=getSignal5(s)
#plot(t,r)

h=filtreRIF('PBande', a=4.9/fe, b=5.1/fe, P=200, fenetre="hamming" )
y = scipy.signal.convolve(s,h,mode='valid')
ny = y.size
ty = numpy.zeros(ny)
for k in range(ny):
    ty[k] = P*te+te*k
figure()
#plot(t,signal,'b')
#plot(t,s,'b')
plot(ty,y,'r')
xlabel('t')
ylabel('y')
axis([0,5,-10,10])


grid()
show()
