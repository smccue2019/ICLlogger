# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ICLloggerUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.GB1 = QtWidgets.QGroupBox(self.centralwidget)
        self.GB1.setGeometry(QtCore.QRect(230, 20, 120, 60))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.GB1.setFont(font)
        self.GB1.setObjectName("GB1")
        self.tip_temp_label = QtWidgets.QLabel(self.GB1)
        self.tip_temp_label.setGeometry(QtCore.QRect(10, 30, 75, 25))
        self.tip_temp_label.setAlignment(QtCore.Qt.AlignCenter)
        self.tip_temp_label.setObjectName("tip_temp_label")
        self.GB2 = QtWidgets.QGroupBox(self.centralwidget)
        self.GB2.setGeometry(QtCore.QRect(230, 100, 120, 60))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.GB2.setFont(font)
        self.GB2.setObjectName("GB2")
        self.housing_temp_label = QtWidgets.QLabel(self.GB2)
        self.housing_temp_label.setGeometry(QtCore.QRect(10, 30, 75, 25))
        self.housing_temp_label.setAlignment(QtCore.Qt.AlignCenter)
        self.housing_temp_label.setObjectName("housing_temp_label")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(30, 90, 100, 25))
        self.startButton.setObjectName("startButton")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(30, 140, 100, 25))
        self.stopButton.setObjectName("stopButton")
        self.quitButton = QtWidgets.QPushButton(self.centralwidget)
        self.quitButton.setGeometry(QtCore.QRect(230, 200, 89, 25))
        self.quitButton.setObjectName("quitButton")
        self.TimeDisplay = QtWidgets.QLabel(self.centralwidget)
        self.TimeDisplay.setGeometry(QtCore.QRect(25, 30, 160, 20))
        self.TimeDisplay.setObjectName("TimeDisplay")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ICL Logger"))
        self.GB1.setTitle(_translate("MainWindow", "Probe Tip"))
        self.tip_temp_label.setText(_translate("MainWindow", "Temp-C"))
        self.GB2.setTitle(_translate("MainWindow", "Probe Housing"))
        self.housing_temp_label.setText(_translate("MainWindow", "Temp-C"))
        self.startButton.setText(_translate("MainWindow", " Start Logging"))
        self.stopButton.setText(_translate("MainWindow", "Stop Logging"))
        self.quitButton.setText(_translate("MainWindow", "Quit"))
        self.TimeDisplay.setText(_translate("MainWindow", "Time"))
