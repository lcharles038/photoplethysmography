import numpy as np
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy.signal import find_peaks
from scipy.interpolate import make_interp_spline

x=[]
y=[]
with open('data/out6_0.csv', 'r') as csvfile:
    i=0
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(i/200)
        y.append(int(row[0]))
        i=i+1
peaks,_ = find_peaks(y, distance=120)

env=[]
for i in range(len(peaks)):
    env.append(y[peaks[i]])
xnew = np.linspace(1,60, 12000)
a_BSpline = make_interp_spline(peaks/200, env)
ynew = a_BSpline(xnew)
plt.plot(x,y,label='signal')
#plt.plot(peaks/200, env, 'r', "peaks")
plt.plot(xnew, ynew,'g', "peaks")
plt.show()
