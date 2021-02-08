# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(903, 912)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 10, 1151, 1091))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.PlotButton = QtWidgets.QPushButton(self.frame)
        self.PlotButton.setGeometry(QtCore.QRect(730, 690, 150, 46))
        self.PlotButton.setObjectName("PlotButton")
        self.BrowseButton = QtWidgets.QPushButton(self.frame)
        self.BrowseButton.setGeometry(QtCore.QRect(570, 690, 150, 46))
        self.BrowseButton.setObjectName("BrowseButton")
        self.UpperLimitButton = QtWidgets.QPushButton(self.frame)
        self.UpperLimitButton.setGeometry(QtCore.QRect(570, 760, 311, 46))
        self.UpperLimitButton.setObjectName("UpperLimitButton")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setGeometry(QtCore.QRect(80, 19, 721, 631))
        self.widget.setObjectName("widget")
        self.mplwidgetPlot = MatplotlibWidget(self.widget)
        self.mplwidgetPlot.setGeometry(QtCore.QRect(70, 60, 571, 451))
        self.mplwidgetPlot.setObjectName("mplwidgetPlot")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(40, 770, 51, 27))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(280, 770, 121, 27))
        self.label.setObjectName("label")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(360, 770, 121, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(20, 700, 521, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(120, 770, 111, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 903, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.PlotButton.setText(_translate("MainWindow", "Plot"))
        self.BrowseButton.setText(_translate("MainWindow", "Browse"))
        self.UpperLimitButton.setText(_translate("MainWindow", "Change Limits"))
        self.label_2.setText(_translate("MainWindow", "Min Count:"))
        self.label.setText(_translate("MainWindow", "Max Count:"))
from matplotlibwidget import MatplotlibWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
