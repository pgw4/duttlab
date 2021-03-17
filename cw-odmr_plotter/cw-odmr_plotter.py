import numpy as np
import matplotlib.pyplot as plt
import time, os
from scipy.optimize import curve_fit
import csv
import re

import datetime

'''Opens .npz data files from CWESR scans, converts to .csv, 
plots average with error bars first (in blue), plots average with lorentz fit (in red) 
second. Lorentz fit requires an initial peak guess  p = np.array(x,x,GUESS)'''

now = datetime.datetime.today()

date = now.strftime('%Y-%m-%d')

#file_name = "2019-12-17-12-51"
file_name = r"2021-03-10-15-42.npz"
#file2 = "2019-08-22-11-05"


#os.chdir("D:\workspace\Data\CW_ESR\\"+date)
data=np.load(file_name)
print(os.curdir+file_name+".npz")

x=data["frequency"][1:]
y=data["scans"][:,1:]
#x2 = data2["frequency"][1:]
#y2= data2["scans"][:,1:]
#print x
#print y
print(np.shape(x))
print(np.shape(y))
#print np.shape(x2)
#print np.shape(y2)
####converting data from npz to matrix###
y_t = np.transpose(y)
xy = np.vstack((x,y))
mat_xy = np.transpose(np.matrix(xy))
#print mat_xy

###### SAVING DATA AS A TXT FILE#########
f = open(file_name + '.txt', 'wb') #update file name in format (sample_yyyymmdd_scannumber); save in current date folder

for line in mat_xy:
    np.savetxt(f,line)

f.close()

#averaging counts from each scan#
mean=sum(y)/len(y)
#mean2 = sum(y2)/len(y2)

sigma = np.std(y)
sem = sigma/np.sqrt(len(y))  #standard error from the mean = std/root(N)


plt.plot(x,mean,'bo-')#,x2,mean2,'r+') #this is the raw plot. Same as what cw_esr gui will show.
plt.errorbar(x,mean,yerr=sem)
plt.show()


def lorentz(x,bg,amp1,x1,gamma1):
    return bg-amp1*gamma1**2/(((x-x1)**2+gamma1**2)) #lorentz = (background-amplitude)*gamma^2/(x-max_guess)^2+gamma^2

def lorentz1(x,bg,amp1,x1,gamma1):
    return (1/np.pi)*(bg-amp1)*(gamma1/2)/((x-x1)**2+(gamma1/2)**2) #lorentz = (1/pi)*(gamma1/2)/((x-x1)**2+(
    # gamma1/2)**2)

func=lorentz

norm=mean/np.average(mean[0:6]) #normalize the data with respect to the first few data points (where the graph is ~flat). Adjust range. Used 0:6 for 200pts in test.

p = np.array([1.0, 0.1, 2.781, 0.01 ]) #Initial guesses: 1 = normalized, 0.1=10% contrast (0.1 amplitude),
# 2.87 (center), 0.01 =???
popt, pcov = curve_fit(func, x, norm, p0 = p) #fit a curve to defined function 'func', x axis = x, using normalized data for analysis, p initial guesses

z=lorentz(x, *popt)

'''removed fit for split data. need a different function or to "focus" on one peak before applying this function.
'''
plt.plot(x, z, 'k-', linewidth=1.5, alpha=0.6, label='Fit')
plt.scatter(x, norm, marker='+', color='r', label='Measured Data') #must plot normalized data
plt.ylabel('AU')
plt.xlabel('RF (GHz)')

print("The fit parameters are:{}".format(popt))
#uncertainties in fit parameters
print("The uncertainties in fit parameters are:{}".format(np.sqrt(np.diag(pcov))))

plt.grid(which='major')
plt.legend(loc=0)
plt.show()







