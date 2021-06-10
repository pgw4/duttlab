from tkinter.filedialog import askopenfilename
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np

root = Tk()

def open():
    filename = askopenfilename()
    data = np.genfromtxt(filename,delimiter='\t')
    x=data[:,0]
    y=data[:,1]
    z=data[:,2]

    xx=x.tolist().count(x[0])
    zz=int(len(z)/xx)
    K=z.reshape(zz,xx).T
    plt.imshow(K,origin='lower',cmap='gist_earth',extent=[min(x),max(x),min(y),max(y)], interpolation='nearest')
    plt.colorbar()
    plt.show()

btn = Button(root, text="Open File", command=open)
btn.pack()
ex = Button(root, text="Exit", command=root.quit)
ex.pack()
root.mainloop()

# Equivalently, we could do that all in one line with:
# x,y,z = np.genfromtxt('14-55-56.txt', delimiter='\t', usecols=(0,1,2))

# x=np.unique(x)
# y=np.unique(y)
# print(x,y)
# X,Y = np.meshgrid(x,y)

# Z=z.reshape(len(y),len(x))
# print(Z.shape)
# plt.pcolormesh(X,Y,Z)
# plt.colorbar()
# plt.show()
