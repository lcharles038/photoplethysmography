from scipy.signal import butter, lfilter, firwin
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz, find_peaks
from numpy import genfromtxt


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def fir_bandPass_filter(data, lowcut, highcut, fs, order=5):
    h = firwin(50, [lowcut,highcut], pass_zero=False, fs=fs, window='boxcar')
    print("h=")
    print (h)
    y=lfilter(h,[1.0], data)
    return y

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    print("a=")
    print (a)
    print("b=")
    print (b)
    y = lfilter(b, a, data)
    return y

# Fréquence échantillonnage pour tous les signaux utilisés, en Hz.
fe = 200
nbPoints = 13625
t = np.linspace(0, nbPoints/200, nbPoints, endpoint=False)

def getSignalEcg(voie1, ordre):
    # Fréquence de coupure basse (volontairement très inférieure à celle du coeur afin de voir la respi...)
    fcBasse = 0.1
    fcHaute = 3.0
    s = butter_bandpass_filter(voie1, fcBasse, fcHaute, fe, order=ordre)
    return s

def getSignalRespiratoire(voie1, ordre):
    # Fréquence de coupure basse (volontairement très inférieure à celle du coeur afin de voir la respi...)
    #fcBasse = 0.12
    #fcHaute = 0.28
    fcBasse = 0.15
    fcHaute = 0.4
    s = butter_bandpass_filter(voie1, fcBasse, fcHaute, fe, order=ordre)
    return s

def getSignalECG_fir(voie1, ordre):
    fcBasse = 0.1
    fcHaute = 10.0
    s = fir_bandPass_filter(voie1, fcBasse, fcHaute, fe, order=ordre)
    return s

def run():
    plt.rcParams['axes.grid'] = True
    voie1 = genfromtxt('data/out6_1.csv', delimiter=',')/1024*5
    voie0 = genfromtxt('data/out6_0.csv', delimiter=',')/1024*5-1.4
    fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, sharex=True)
    ax1.plot(t[10*fe:60*fe], (voie1)[10*fe:60*fe], 'deepskyblue',label='signal brut (V)', )
    ax1.legend(loc='upper right')
    ax2.plot(t[10*fe:60*fe], (voie0)[10*fe:60*fe], 'lightgreen', label='signal ECG filtré analogiquement')
    ax2.legend(loc='upper right')
    peaks,_ = (find_peaks((-68*getSignalEcg(voie1, 3))[10*fe:60*fe], distance=0.6*fe))
    print (peaks)
    bpm=[]
    for i in range (len(peaks)-1):
        bpm.append(60/(peaks[i+1]-peaks[i])*fe)
    bpm.append(70)
    for x in bpm:
        print(str(x))
    # correctionq
    bpm[14] = 68.76
    bpm[15] = 70
    ax3.plot(t[10*fe:60*fe], (-68*getSignalEcg(voie1, 3))[10*fe:60*fe], 'chocolate', label='signal ECG filtré numériquement')
    ax3.plot((10 + peaks/fe), (-68*getSignalEcg(voie1, 3))[10*fe:60*fe][peaks],"x")
    ax3.legend(loc='upper right')
    ax4.step((10.6 + peaks/fe), bpm)
    tck = interpolate.splrep((10.6 + peaks/fe), bpm)
    bpmlisse=[]
    for top in t[10*fe:60*fe]:
        bpmlisse.append(interpolate.splev(top, tck))
    ax4.plot(t[10*fe:60*fe], bpmlisse)
    ax5.plot(t[10*fe:60*fe], (-getSignalRespiratoire(voie1, 3))[10*fe:60*fe], 'darkmagenta')
    ax5.legend(loc='lower right')
    ax6.plot(t[10*fe:60*fe], (-68*getSignalECG_fir(voie1, 3))[10*fe:60*fe], 'darkmagenta', label='signal cardiaque filtré numériquement 2')
    ax6.legend(loc='lower right')
    plt.xlabel('Temps (secondes)')
    fig.suptitle('Les différents traitements du signal obtenu')
    #plt.hlines([-a, a], 0, 0.005, linestyles='--')
    plt.grid(True)
    plt.show()


run()
