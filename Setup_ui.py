# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Setup_ui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_For_Setup(object):
    def setupUi(self, Dialo):
        Dialo.setObjectName("Dialo")
        Dialo.resize(540, 406)
        font = QtGui.QFont()
        font.setFamily("黑体")
        Dialo.setFont(font)
        Dialo.setSizeGripEnabled(False)
        self.editServerIP = QtWidgets.QLineEdit(Dialo)
        self.editServerIP.setGeometry(QtCore.QRect(160, 250, 251, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.editServerIP.setFont(font)
        self.editServerIP.setText("127.0.0.1")
        self.editServerIP.setClearButtonEnabled(False)
        self.editServerIP.setObjectName("editServerIP")
        self.editServerPort = QtWidgets.QLineEdit(Dialo)
        self.editServerPort.setGeometry(QtCore.QRect(160, 300, 251, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.editServerPort.setFont(font)
        self.editServerPort.setText("20000")
        self.editServerPort.setObjectName("editServerPort")
        self.backgroundPic = QtWidgets.QWidget(Dialo)
        self.backgroundPic.setGeometry(QtCore.QRect(0, 0, 541, 221))
        self.backgroundPic.setObjectName("backgroundPic")
        self.closeBt = QtWidgets.QToolButton(self.backgroundPic)
        self.closeBt.setGeometry(QtCore.QRect(510, 0, 31, 41))
        self.closeBt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.closeBt.setText("")
        self.closeBt.setCheckable(False)
        self.closeBt.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.closeBt.setAutoRaise(True)
        self.closeBt.setObjectName("closeBt")
        self.minBt = QtWidgets.QToolButton(self.backgroundPic)
        self.minBt.setGeometry(QtCore.QRect(480, 0, 31, 41))
        self.minBt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.minBt.setText("")
        self.minBt.setAutoRaise(True)
        self.minBt.setObjectName("minBt")
        self.lblSetup = QtWidgets.QLabel(Dialo)
        self.lblSetup.setGeometry(QtCore.QRect(20, 220, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lblSetup.setFont(font)
        self.lblSetup.setObjectName("lblSetup")
        self.lblIP = QtWidgets.QLabel(Dialo)
        self.lblIP.setGeometry(QtCore.QRect(60, 260, 91, 16))
        self.lblIP.setObjectName("lblIP")
        self.lblPort = QtWidgets.QLabel(Dialo)
        self.lblPort.setGeometry(QtCore.QRect(60, 310, 91, 16))
        self.lblPort.setObjectName("lblPort")
        self.pbCancel = QtWidgets.QPushButton(Dialo)
        self.pbCancel.setGeometry(QtCore.QRect(430, 370, 93, 28))
        self.pbCancel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pbCancel.setObjectName("pbCancel")
        self.pbConfirm = QtWidgets.QPushButton(Dialo)
        self.pbConfirm.setGeometry(QtCore.QRect(330, 370, 93, 28))
        self.pbConfirm.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pbConfirm.setObjectName("pbConfirm")

        self.retranslateUi(Dialo)
        QtCore.QMetaObject.connectSlotsByName(Dialo)

    def retranslateUi(self, Dialo):
        _translate = QtCore.QCoreApplication.translate
        Dialo.setWindowTitle(_translate("Dialo", "Dialog"))
        self.editServerIP.setToolTip(_translate("Dialo", "Please enter the server address"))
        self.editServerPort.setToolTip(_translate("Dialo", "Please enter the server port"))
        self.closeBt.setToolTip(_translate("Dialo", "Exit"))
        self.minBt.setToolTip(_translate("Dialo", "Minimize"))
        self.lblSetup.setText(_translate("Dialo", "Network settings"))
        self.lblIP.setText(_translate("Dialo", "Server address :"))
        self.lblPort.setText(_translate("Dialo", "Server port :"))
        self.pbCancel.setText(_translate("Dialo", "Cancel"))
        self.pbConfirm.setText(_translate("Dialo", "Confirm"))

