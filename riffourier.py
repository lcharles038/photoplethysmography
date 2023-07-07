import numpy
import math
import scipy.signal

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



