'''
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from gui import Ui_MainWindow


class MyForm(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


# Opens the GUI
app = QApplication(sys.argv)
myapp = MyForm()

# Shows the GUI
myapp.show()

# Exits the GUI when the x button is clicked
sys.exit(app.exec_())
'''

import sys

from PyQt5 import QtCore, QtWidgets, QtGui, uic
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar, FigureCanvasQTAgg as FigureCanvas
#from pylab import *
#from matplotlib.backends.backend_qt4agg import (FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as
# NavigationToolbar)
import numpy as np

from pathlib import Path
thisdir = Path('.')

qtCreatorFile = thisdir / "gui.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        #QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.mplwidgetPlot.axes.set_title("Confocal Image",fontsize=15)
        self.ui.mplwidgetPlot.axes.set_xlabel("X-axis",fontsize=15)
        self.ui.mplwidgetPlot.axes.set_ylabel("Y-axis",fontsize=15)

        self.canvas = FigureCanvas(self.ui.mplwidgetPlot.figure)
        self.canvas.setParent(self.ui.widget)
        # self.canvas.setFocusPolicy(Qt.StrongFocus)
        # self.canvas.setFocus()

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.ui.widget)

        # self.canvas.mpl_connect('key_press_event', self.on_key_press)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.canvas)  # the matplotlib canvas
        vbox.addWidget(self.mpl_toolbar)
        self.ui.widget.setLayout(vbox)

        self.ui.mplwidgetPlot = self.canvas

        self.ui.PlotButton.clicked.connect(self.PlotImage)
        self.ui.BrowseButton.clicked.connect(self.SingleBrowse)
        self.ui.UpperLimitButton.clicked.connect(self.UpperLimit)
        #self.connect(self.ui.BrowseButton, QtCore.SIGNAL("clicked()"), self.SingleBrowse)
        #self.connect(self.ui.PlotButton, QtCore.SIGNAL("clicked()"), self.PlotImage)
        #self.connect(self.ui.UpperLimitButton, QtCore.SIGNAL("clicked()"), self.UpperLimit)
        self.ui.lineEdit_3.setText('0')
        self.ui.lineEdit_2.setText('1000')

    def SingleBrowse(self):
        pass
        #self.filePath = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File',"C:\Python Programs\\test_ui\\")
        #self.ui.lineEdit.setText(self.filePath)


        #fileHandle = open(filePath, 'r')
        #lines = fileHandle.readlines()
        #for line in lines:
            #print(line)


    def PlotImage(self):

        # path="D:\\VSCode\\image_viewer-master\\source\\test.txt"
        # x,y,z = [], [], []
        # lines=open(path, 'r').readlines()
        # for line in lines:
        #     xx,yy,zz = line.split('\t')
        #     x.append(xx)
        #     y.append(yy)
        #     z.append(zz)

        self.filePath = r"D:\Code\duttlab\image_plotter\old\test.txt"
        self.reset_plot()
        print((self.filePath))
        X, Y, Z = np.loadtxt(str(self.filePath), dtype=str, delimiter='\n')

        x = X.split('\t')
        y = Y.split('\t')
        z = Z.split('\t')

        x = x[0:len(x) - 1]
        y = y[0:len(y) - 1]
        z = z[0:len(z) - 1]

        x = list(map(float, x))
        y = list(map(float, y))
        N = len(x)
        counts = list(map(float, z))
        if len(counts)/N == N:
            counts = np.reshape(counts, (N , N))
        else:
            counts = np.reshape(counts, (N-1, N))

        # Change the unit in microns
        x=(x-np.average(x))*11.0  # 11um/V is the magnification when the Olympus 0.95 dry objective is in the Cryo table-setup.
        y=(y-np.average(y))*11.0

        # Sets up the pcolormesh plot with a copper color scheme.
        image = self.axes.pcolormesh(x, y, counts, cmap='copper')
        self.axes.tick_params(axis='both', labelsize=15)

        # Creates a colorbar legend for the plot.
        cbar=self.ui.mplwidgetPlot.figure.colorbar(image)
        ax=self.axes
        cbar.ax.tick_params(labelsize=15)


        # Redefine the axes
        self.axes.set_xlabel("X (Microns)",fontsize=11)
        self.axes.set_title("Confocal Image",fontsize=15)
        self.axes.set_ylabel("Y (Microns)",fontsize=11)

        # Draws the new plot.
        self.ui.mplwidgetPlot.draw()
        print(N)

    def UpperLimit(self):

        self.reset_plot()
        print((self.filePath))
        X, Y, Z = np.loadtxt(str(self.filePath), dtype=str, delimiter='\n')

        x = X.split('\t')
        y = Y.split('\t')
        z = Z.split('\t')

        x = x[0:len(x) - 1]
        y = y[0:len(y) - 1]
        z = z[0:len(z) - 1]

        x = list(map(float, x))
        y = list(map(float, y))
        N = len(x)
        counts = list(map(float, z))
        if len(counts)/N == N:
            counts = np.reshape(counts, (N , N))
        else:
            counts = np.reshape(counts, (N-1, N))

        # Change the unit in microns
        x=(x-np.average(x))*11.0  # 11um/V is the magnification when the Olympus 0.95 dry objective is in the Cryo table-setup.
        y=(y-np.average(y))*11.0

        lowerlimit= float(self.ui.lineEdit_3.text())
        upperlimit= float(self.ui.lineEdit_2.text())
        counts=np.clip(counts,lowerlimit,upperlimit)


        # Sets up the pcolormesh plot with a copper color scheme.
        image = self.axes.pcolormesh(x, y, counts, cmap=cm.copper)
        self.axes.tick_params(axis='both', labelsize=15)

        # Creates a colorbar legend for the plot.
        cbar=self.ui.mplwidgetPlot.figure.colorbar(image)
        ax=self.axes
        cbar.ax.tick_params(labelsize=20)


        # Redefine the axes
        self.axes.set_xlabel("X (Microns)",fontsize=11)
        self.axes.set_title("Confocal Image",fontsize=15)
        self.axes.set_ylabel("Y (Microns)",fontsize=11)

        # Draws the new plot.
        self.ui.mplwidgetPlot.draw()

    def reset_plot(self):
        self.ui.mplwidgetPlot.figure.clear()
        self.axes = self.ui.mplwidgetPlot.figure.add_subplot(111)

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"

        # Creates a message box that displays the quit_msg and has two pushButtons
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                     quit_msg, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        # Yes means the user wants to quit. Thus the window is closed.
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()

        # No means the event is ignored and the window stays open.
        else:
            event.ignore()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    #window.setGeometry(0,0,500,300)
    #window.setWindowTitle("PyQT")
    window.show()
    sys.exit(app.exec_())