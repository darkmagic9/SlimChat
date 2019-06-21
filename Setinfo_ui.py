# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Setinfo_ui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_For_Setinfo(object):
    def setupUi(self, Dialo):
        Dialo.setObjectName("Dialo")
        Dialo.resize(540, 406)
        font = QtGui.QFont()
        font.setFamily("黑体")
        Dialo.setFont(font)
        Dialo.setSizeGripEnabled(False)
        self.editName = QtWidgets.QLineEdit(Dialo)
        self.editName.setGeometry(QtCore.QRect(190, 128, 251, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.editName.setFont(font)
        self.editName.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.editName.setText("")
        self.editName.setPlaceholderText("Please enter your nickname")
        self.editName.setClearButtonEnabled(False)
        self.editName.setObjectName("editName")
        self.top = QtWidgets.QWidget(Dialo)
        self.top.setGeometry(QtCore.QRect(0, 0, 541, 81))
        self.top.setObjectName("top")
        self.closeBt = QtWidgets.QToolButton(self.top)
        self.closeBt.setGeometry(QtCore.QRect(510, 0, 31, 41))
        self.closeBt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.closeBt.setText("")
        self.closeBt.setCheckable(False)
        self.closeBt.setPopupMode(QtWidgets.QToolButton.DelayedPopup)
        self.closeBt.setAutoRaise(True)
        self.closeBt.setObjectName("closeBt")
        self.btDone = QtWidgets.QPushButton(Dialo)
        self.btDone.setGeometry(QtCore.QRect(150, 320, 251, 41))
        self.btDone.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btDone.setDefault(True)
        self.btDone.setFlat(False)
        self.btDone.setObjectName("btDone")
        self.lblhead = QtWidgets.QLabel(Dialo)
        self.lblhead.setGeometry(QtCore.QRect(240, 190, 111, 111))
        self.lblhead.setText("")
        self.lblhead.setScaledContents(True)
        self.lblhead.setObjectName("lblhead")
        self.label_2 = QtWidgets.QLabel(Dialo)
        self.label_2.setGeometry(QtCore.QRect(90, 200, 91, 16))
        self.label_2.setObjectName("label_2")
        self.scanPic = QtWidgets.QPushButton(Dialo)
        self.scanPic.setGeometry(QtCore.QRect(80, 250, 93, 28))
        self.scanPic.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.scanPic.setFlat(False)
        self.scanPic.setObjectName("scanPic")
        self.label_3 = QtWidgets.QLabel(Dialo)
        self.label_3.setGeometry(QtCore.QRect(90, 140, 72, 15))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Dialo)
        QtCore.QMetaObject.connectSlotsByName(Dialo)

    def retranslateUi(self, Dialo):
        _translate = QtCore.QCoreApplication.translate
        Dialo.setWindowTitle(_translate("Dialo", "Dialog"))
        self.editName.setToolTip(_translate("Dialo", "Please enter a new nickname"))
        self.closeBt.setToolTip(_translate("Dialo", "Exit"))
        self.btDone.setToolTip(_translate("Dialo", "Complete"))
        self.btDone.setText(_translate("Dialo", "Complete"))
        self.label_2.setText(_translate("Dialo", "Set Avatar"))
        self.scanPic.setToolTip(_translate("Dialo", "Browse"))
        self.scanPic.setText(_translate("Dialo", "Browse"))
        self.label_3.setText(_translate("Dialo", "Set nickname"))

