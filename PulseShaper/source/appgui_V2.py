# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'source/appgui_V2.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_quantumpulse(object):
    def setupUi(self, quantumpulse):
        quantumpulse.setObjectName("quantumpulse")
        quantumpulse.resize(1256, 730)
        self.centralwidget = QtWidgets.QWidget(quantumpulse)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 611, 181))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.metadatatextEdit = QtWidgets.QTextEdit(self.groupBox)
        self.metadatatextEdit.setGeometry(QtCore.QRect(20, 60, 591, 87))
        self.metadatatextEdit.setObjectName("metadatatextEdit")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setGeometry(QtCore.QRect(0, 150, 611, 311))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(630, 10, 601, 451))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.dataMPL = QtWidgets.QWidget(self.groupBox_2)
        self.dataMPL.setGeometry(QtCore.QRect(20, 40, 571, 331))
        self.dataMPL.setObjectName("dataMPL")
        self.pushButtonSaveData = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButtonSaveData.setGeometry(QtCore.QRect(20, 390, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pushButtonSaveData.setFont(font)
        self.pushButtonSaveData.setObjectName("pushButtonSaveData")
        self.checkBoxAutoSave = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBoxAutoSave.setGeometry(QtCore.QRect(140, 393, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.checkBoxAutoSave.setFont(font)
        self.checkBoxAutoSave.setObjectName("checkBoxAutoSave")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 470, 601, 211))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.trackingMPL = QtWidgets.QWidget(self.groupBox_3)
        self.trackingMPL.setGeometry(QtCore.QRect(20, 70, 571, 131))
        self.trackingMPL.setObjectName("trackingMPL")
        self.lineEditSig = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditSig.setGeometry(QtCore.QRect(70, 40, 61, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEditSig.setFont(font)
        self.lineEditSig.setObjectName("lineEditSig")
        self.lineEditRef = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditRef.setGeometry(QtCore.QRect(280, 40, 61, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEditRef.setFont(font)
        self.lineEditRef.setObjectName("lineEditRef")
        self.lineEditThreshold = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEditThreshold.setGeometry(QtCore.QRect(480, 40, 61, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEditThreshold.setFont(font)
        self.lineEditThreshold.setObjectName("lineEditThreshold")
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setGeometry(QtCore.QRect(30, 40, 53, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setGeometry(QtCore.QRect(210, 40, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_9 = QtWidgets.QLabel(self.groupBox_3)
        self.label_9.setGeometry(QtCore.QRect(410, 40, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.pushButtonStart = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStart.setEnabled(False)
        self.pushButtonStart.setGeometry(QtCore.QRect(930, 490, 121, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButtonStart.setFont(font)
        self.pushButtonStart.setObjectName("pushButtonStart")
        self.pushButtonStop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStop.setGeometry(QtCore.QRect(1070, 490, 121, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButtonStop.setFont(font)
        self.pushButtonStop.setObjectName("pushButtonStop")
        self.pushButtonUpload = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonUpload.setGeometry(QtCore.QRect(780, 490, 121, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButtonUpload.setFont(font)
        self.pushButtonUpload.setObjectName("pushButtonUpload")
        self.pushButtonReady = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonReady.setGeometry(QtCore.QRect(660, 490, 121, 91))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButtonReady.setFont(font)
        self.pushButtonReady.setObjectName("pushButtonReady")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(920, 620, 59, 16))
        self.label.setObjectName("label")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(20, 190, 591, 251))
        self.tabWidget.setObjectName("tabWidget")
        self.PTStab = QtWidgets.QWidget()
        self.PTStab.setObjectName("PTStab")
        self.lineEditPTSFreq = QtWidgets.QLineEdit(self.PTStab)
        self.lineEditPTSFreq.setEnabled(False)
        self.lineEditPTSFreq.setGeometry(QtCore.QRect(20, 60, 81, 22))
        self.lineEditPTSFreq.setObjectName("lineEditPTSFreq")
        self.label_17 = QtWidgets.QLabel(self.PTStab)
        self.label_17.setGeometry(QtCore.QRect(20, 40, 101, 16))
        self.label_17.setObjectName("label_17")
        self.checkBoxUsePTS = QtWidgets.QCheckBox(self.PTStab)
        self.checkBoxUsePTS.setGeometry(QtCore.QRect(20, 10, 87, 20))
        self.checkBoxUsePTS.setChecked(True)
        self.checkBoxUsePTS.setObjectName("checkBoxUsePTS")
        self.tabWidget.addTab(self.PTStab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.checkBoxUseSRS = QtWidgets.QCheckBox(self.tab_3)
        self.checkBoxUseSRS.setEnabled(True)
        self.checkBoxUseSRS.setGeometry(QtCore.QRect(20, 10, 87, 20))
        self.checkBoxUseSRS.setObjectName("checkBoxUseSRS")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.voltageSlider = QtWidgets.QSlider(self.tab_2)
        self.voltageSlider.setGeometry(QtCore.QRect(20, 30, 201, 22))
        self.voltageSlider.setMinimum(0)
        self.voltageSlider.setMaximum(1000)
        self.voltageSlider.setSingleStep(5)
        self.voltageSlider.setProperty("value", 99)
        self.voltageSlider.setOrientation(QtCore.Qt.Horizontal)
        self.voltageSlider.setInvertedAppearance(False)
        self.voltageSlider.setInvertedControls(False)
        self.voltageSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.voltageSlider.setObjectName("voltageSlider")
        self.comboBoxTimeRes = QtWidgets.QComboBox(self.tab_2)
        self.comboBoxTimeRes.setGeometry(QtCore.QRect(130, 80, 51, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.comboBoxTimeRes.setFont(font)
        self.comboBoxTimeRes.setObjectName("comboBoxTimeRes")
        self.comboBoxTimeRes.addItem("")
        self.comboBoxTimeRes.addItem("")
        self.comboBoxTimeRes.addItem("")
        self.comboBoxTimeRes.addItem("")
        self.comboBoxTimeRes.addItem("")
        self.label_29 = QtWidgets.QLabel(self.tab_2)
        self.label_29.setGeometry(QtCore.QRect(130, 60, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.label_30 = QtWidgets.QLabel(self.tab_2)
        self.label_30.setGeometry(QtCore.QRect(180, 80, 53, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.label_19 = QtWidgets.QLabel(self.tab_2)
        self.label_19.setGeometry(QtCore.QRect(30, 10, 101, 16))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(self.tab_2)
        self.label_20.setGeometry(QtCore.QRect(10, 40, 53, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(self.tab_2)
        self.label_21.setGeometry(QtCore.QRect(220, 40, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.lineEditPulsewidth = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditPulsewidth.setGeometry(QtCore.QRect(10, 80, 81, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEditPulsewidth.setFont(font)
        self.lineEditPulsewidth.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditPulsewidth.setObjectName("lineEditPulsewidth")
        self.label_31 = QtWidgets.QLabel(self.tab_2)
        self.label_31.setGeometry(QtCore.QRect(10, 60, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.label_32 = QtWidgets.QLabel(self.tab_2)
        self.label_32.setGeometry(QtCore.QRect(100, 80, 53, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.awgSelectcomboBox = QtWidgets.QComboBox(self.tab_2)
        self.awgSelectcomboBox.setGeometry(QtCore.QRect(260, 30, 104, 26))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.awgSelectcomboBox.setFont(font)
        self.awgSelectcomboBox.setMaxVisibleItems(2)
        self.awgSelectcomboBox.setMaxCount(2)
        self.awgSelectcomboBox.setObjectName("awgSelectcomboBox")
        self.awgSelectcomboBox.addItem("")
        self.awgSelectcomboBox.addItem("")
        self.pulseshapecomboBox = QtWidgets.QComboBox(self.tab_2)
        self.pulseshapecomboBox.setGeometry(QtCore.QRect(260, 70, 104, 26))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pulseshapecomboBox.setFont(font)
        self.pulseshapecomboBox.setMaxVisibleItems(4)
        self.pulseshapecomboBox.setMaxCount(4)
        self.pulseshapecomboBox.setObjectName("pulseshapecomboBox")
        self.pulseshapecomboBox.addItem("")
        self.pulseshapecomboBox.addItem("")
        self.pulseshapecomboBox.addItem("")
        self.pulseshapecomboBox.addItem("")
        self.label_33 = QtWidgets.QLabel(self.tab_2)
        self.label_33.setGeometry(QtCore.QRect(270, 20, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.label_34 = QtWidgets.QLabel(self.tab_2)
        self.label_34.setGeometry(QtCore.QRect(270, 60, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_34.setFont(font)
        self.label_34.setObjectName("label_34")
        self.lineEditSBfreq = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditSBfreq.setEnabled(True)
        self.lineEditSBfreq.setGeometry(QtCore.QRect(240, 150, 81, 22))
        self.lineEditSBfreq.setObjectName("lineEditSBfreq")
        self.label_35 = QtWidgets.QLabel(self.tab_2)
        self.label_35.setGeometry(QtCore.QRect(240, 130, 111, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_35.setFont(font)
        self.label_35.setObjectName("label_35")
        self.checkBoxIQmod = QtWidgets.QCheckBox(self.tab_2)
        self.checkBoxIQmod.setEnabled(True)
        self.checkBoxIQmod.setGeometry(QtCore.QRect(10, 110, 111, 21))
        self.checkBoxIQmod.setObjectName("checkBoxIQmod")
        self.lineEditIQscale = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditIQscale.setEnabled(True)
        self.lineEditIQscale.setGeometry(QtCore.QRect(240, 110, 81, 22))
        self.lineEditIQscale.setObjectName("lineEditIQscale")
        self.lineEditSkewPhase = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditSkewPhase.setEnabled(True)
        self.lineEditSkewPhase.setGeometry(QtCore.QRect(370, 150, 81, 22))
        self.lineEditSkewPhase.setObjectName("lineEditSkewPhase")
        self.label_36 = QtWidgets.QLabel(self.tab_2)
        self.label_36.setGeometry(QtCore.QRect(240, 90, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_36.setFont(font)
        self.label_36.setObjectName("label_36")
        self.label_37 = QtWidgets.QLabel(self.tab_2)
        self.label_37.setGeometry(QtCore.QRect(370, 130, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_37.setFont(font)
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(self.tab_2)
        self.label_38.setGeometry(QtCore.QRect(340, 90, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_38.setFont(font)
        self.label_38.setObjectName("label_38")
        self.lineEditPhase = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditPhase.setEnabled(True)
        self.lineEditPhase.setGeometry(QtCore.QRect(340, 110, 81, 22))
        self.lineEditPhase.setObjectName("lineEditPhase")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setGeometry(QtCore.QRect(20, 0, 241, 71))
        self.textBrowser.setObjectName("textBrowser")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_5.setGeometry(QtCore.QRect(320, 0, 211, 231))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setObjectName("groupBox_5")
        self.label_7 = QtWidgets.QLabel(self.groupBox_5)
        self.label_7.setGeometry(QtCore.QRect(20, 120, 53, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.lineEditScanStop = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEditScanStop.setGeometry(QtCore.QRect(90, 120, 81, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEditScanStop.setFont(font)
        self.lineEditScanStop.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditScanStop.setObjectName("lineEditScanStop")
        self.label_6 = QtWidgets.QLabel(self.groupBox_5)
        self.label_6.setGeometry(QtCore.QRect(20, 60, 53, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lineEditScanNum = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEditScanNum.setGeometry(QtCore.QRect(120, 150, 81, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEditScanNum.setFont(font)
        self.lineEditScanNum.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditScanNum.setObjectName("lineEditScanNum")
        self.label_5 = QtWidgets.QLabel(self.groupBox_5)
        self.label_5.setGeometry(QtCore.QRect(20, 90, 53, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEditScanStep = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEditScanStep.setGeometry(QtCore.QRect(90, 90, 81, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEditScanStep.setFont(font)
        self.lineEditScanStep.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditScanStep.setObjectName("lineEditScanStep")
        self.label_8 = QtWidgets.QLabel(self.groupBox_5)
        self.label_8.setGeometry(QtCore.QRect(20, 150, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.lineEditScanStart = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEditScanStart.setGeometry(QtCore.QRect(90, 60, 81, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEditScanStart.setFont(font)
        self.lineEditScanStart.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditScanStart.setObjectName("lineEditScanStart")
        self.lineEditAvgNum = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEditAvgNum.setGeometry(QtCore.QRect(120, 180, 81, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lineEditAvgNum.setFont(font)
        self.lineEditAvgNum.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditAvgNum.setObjectName("lineEditAvgNum")
        self.label_10 = QtWidgets.QLabel(self.groupBox_5)
        self.label_10.setGeometry(QtCore.QRect(20, 180, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.scantypecomboBox = QtWidgets.QComboBox(self.tab)
        self.scantypecomboBox.setGeometry(QtCore.QRect(30, 90, 181, 32))
        self.scantypecomboBox.setEditable(True)
        self.scantypecomboBox.setMaxCount(6)
        self.scantypecomboBox.setObjectName("scantypecomboBox")
        self.scantypecomboBox.addItem("")
        self.scantypecomboBox.addItem("")
        self.scantypecomboBox.addItem("")
        self.scantypecomboBox.addItem("")
        self.scantypecomboBox.addItem("")
        self.scantypecomboBox.addItem("")
        self.tabWidget.addTab(self.tab, "")
        self.lineEditSamples = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditSamples.setGeometry(QtCore.QRect(30, 450, 113, 21))
        self.lineEditSamples.setObjectName("lineEditSamples")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(30, 430, 59, 16))
        self.label_11.setObjectName("label_11")
        self.lineEditCountTime = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditCountTime.setGeometry(QtCore.QRect(170, 450, 113, 21))
        self.lineEditCountTime.setObjectName("lineEditCountTime")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(170, 430, 101, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(330, 430, 101, 16))
        self.label_13.setObjectName("label_13")
        self.lineEditResetTime = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditResetTime.setGeometry(QtCore.QRect(330, 450, 113, 21))
        self.lineEditResetTime.setObjectName("lineEditResetTime")
        quantumpulse.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(quantumpulse)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1256, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        quantumpulse.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(quantumpulse)
        self.statusbar.setObjectName("statusbar")
        quantumpulse.setStatusBar(self.statusbar)
        self.actionSettings = QtWidgets.QAction(quantumpulse)
        self.actionSettings.setObjectName("actionSettings")
        self.actionExit = QtWidgets.QAction(quantumpulse)
        self.actionExit.setObjectName("actionExit")
        self.actionSave_Defaults = QtWidgets.QAction(quantumpulse)
        self.actionSave_Defaults.setObjectName("actionSave_Defaults")
        self.menuFile.addAction(self.actionSave_Defaults)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.retranslateUi(quantumpulse)
        self.tabWidget.setCurrentIndex(2)
        self.awgSelectcomboBox.setCurrentIndex(0)
        self.pulseshapecomboBox.setCurrentIndex(0)
        self.scantypecomboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(quantumpulse)

    def retranslateUi(self, quantumpulse):
        _translate = QtCore.QCoreApplication.translate
        quantumpulse.setWindowTitle(_translate("quantumpulse", "Pulseshaper App"))
        self.groupBox.setTitle(_translate("quantumpulse", "Sequence"))
        self.label_2.setText(_translate("quantumpulse", "Definition"))
        self.groupBox_4.setTitle(_translate("quantumpulse", "Microwave"))
        self.groupBox_2.setTitle(_translate("quantumpulse", "Data"))
        self.pushButtonSaveData.setText(_translate("quantumpulse", "Save Data"))
        self.checkBoxAutoSave.setText(_translate("quantumpulse", "Auto Save"))
        self.groupBox_3.setTitle(_translate("quantumpulse", "Tracking"))
        self.label_3.setText(_translate("quantumpulse", "Signal"))
        self.label_4.setText(_translate("quantumpulse", "Reference"))
        self.label_9.setText(_translate("quantumpulse", "Threshold"))
        self.pushButtonStart.setText(_translate("quantumpulse", "Start"))
        self.pushButtonStop.setText(_translate("quantumpulse", "Stop"))
        self.pushButtonUpload.setText(_translate("quantumpulse", "Upload"))
        self.pushButtonReady.setText(_translate("quantumpulse", "Ready"))
        self.label.setText(_translate("quantumpulse", "Scan type"))
        self.label_17.setText(_translate("quantumpulse", "Frequency (GHz)"))
        self.checkBoxUsePTS.setText(_translate("quantumpulse", "Use this"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PTStab), _translate("quantumpulse", "PTS"))
        self.checkBoxUseSRS.setText(_translate("quantumpulse", "Use this"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("quantumpulse", "SRS"))
        self.comboBoxTimeRes.setItemText(0, _translate("quantumpulse", "1"))
        self.comboBoxTimeRes.setItemText(1, _translate("quantumpulse", "5"))
        self.comboBoxTimeRes.setItemText(2, _translate("quantumpulse", "10"))
        self.comboBoxTimeRes.setItemText(3, _translate("quantumpulse", "25"))
        self.comboBoxTimeRes.setItemText(4, _translate("quantumpulse", "100"))
        self.label_29.setText(_translate("quantumpulse", "Time Resolution"))
        self.label_30.setText(_translate("quantumpulse", "ns"))
        self.label_19.setText(_translate("quantumpulse", "Amplitude"))
        self.label_20.setText(_translate("quantumpulse", "0 V"))
        self.label_21.setText(_translate("quantumpulse", "1 V"))
        self.lineEditPulsewidth.setText(_translate("quantumpulse", "20"))
        self.label_31.setText(_translate("quantumpulse", "Pulse width"))
        self.label_32.setText(_translate("quantumpulse", "ns"))
        self.awgSelectcomboBox.setItemText(0, _translate("quantumpulse", "AWG 520"))
        self.awgSelectcomboBox.setItemText(1, _translate("quantumpulse", "AWG 5014c"))
        self.pulseshapecomboBox.setItemText(0, _translate("quantumpulse", "Square"))
        self.pulseshapecomboBox.setItemText(1, _translate("quantumpulse", "Gaussian"))
        self.pulseshapecomboBox.setItemText(2, _translate("quantumpulse", "Sech"))
        self.pulseshapecomboBox.setItemText(3, _translate("quantumpulse", "Load Wfm"))
        self.label_33.setText(_translate("quantumpulse", "AWG device"))
        self.label_34.setText(_translate("quantumpulse", "Pulseshape"))
        self.lineEditSBfreq.setText(_translate("quantumpulse", "10"))
        self.label_35.setText(_translate("quantumpulse", "Sideband frequency (MHz)"))
        self.checkBoxIQmod.setText(_translate("quantumpulse", "I/Q modulation"))
        self.lineEditIQscale.setText(_translate("quantumpulse", "1.0"))
        self.lineEditSkewPhase.setText(_translate("quantumpulse", "0.0"))
        self.label_36.setText(_translate("quantumpulse", "IQ scale factor"))
        self.label_37.setText(_translate("quantumpulse", "skew phase (deg)"))
        self.label_38.setText(_translate("quantumpulse", "phase (deg)"))
        self.lineEditPhase.setText(_translate("quantumpulse", "0.0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("quantumpulse", "AWG"))
        self.textBrowser.setHtml(_translate("quantumpulse", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.SF NS Text\'; font-size:9pt;\">Amplitude: use mV</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.SF NS Text\'; font-size:9pt;\">Freq: use MHz</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.SF NS Text\'; font-size:9pt;\">time: use ns </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'.SF NS Text\'; font-size:9pt;\">number: use integers from 1 to 50</span></p></body></html>"))
        self.groupBox_5.setTitle(_translate("quantumpulse", "Scan parameters"))
        self.label_7.setText(_translate("quantumpulse", "Stop"))
        self.lineEditScanStop.setText(_translate("quantumpulse", "0"))
        self.label_6.setText(_translate("quantumpulse", "Start"))
        self.lineEditScanNum.setText(_translate("quantumpulse", "0"))
        self.label_5.setText(_translate("quantumpulse", "Step"))
        self.lineEditScanStep.setText(_translate("quantumpulse", "1"))
        self.label_8.setText(_translate("quantumpulse", "# of Steps"))
        self.lineEditScanStart.setText(_translate("quantumpulse", "0"))
        self.lineEditAvgNum.setText(_translate("quantumpulse", "0"))
        self.label_10.setText(_translate("quantumpulse", "# of Averages"))
        self.scantypecomboBox.setCurrentText(_translate("quantumpulse", "Amplitude"))
        self.scantypecomboBox.setItemText(0, _translate("quantumpulse", "Amplitude"))
        self.scantypecomboBox.setItemText(1, _translate("quantumpulse", "Time"))
        self.scantypecomboBox.setItemText(2, _translate("quantumpulse", "Number of pulses"))
        self.scantypecomboBox.setItemText(3, _translate("quantumpulse", "Carrier frequency"))
        self.scantypecomboBox.setItemText(4, _translate("quantumpulse", "Sideband frequency"))
        self.scantypecomboBox.setItemText(5, _translate("quantumpulse", "Pulsewidth"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("quantumpulse", "Scan "))
        self.lineEditSamples.setText(_translate("quantumpulse", "50000"))
        self.label_11.setText(_translate("quantumpulse", "Samples"))
        self.lineEditCountTime.setText(_translate("quantumpulse", "300"))
        self.label_12.setText(_translate("quantumpulse", "Count time (ns)"))
        self.label_13.setText(_translate("quantumpulse", "Reset time (ns)"))
        self.lineEditResetTime.setText(_translate("quantumpulse", "2000"))
        self.menuFile.setTitle(_translate("quantumpulse", "File"))
        self.actionSettings.setText(_translate("quantumpulse", "Settings..."))
        self.actionExit.setText(_translate("quantumpulse", "Exit"))
        self.actionSave_Defaults.setText(_translate("quantumpulse", "Save Defaults"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    quantumpulse = QtWidgets.QMainWindow()
    ui = Ui_quantumpulse()
    ui.setupUi(quantumpulse)
    quantumpulse.show()
    sys.exit(app.exec_())
