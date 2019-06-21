# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Additem_ui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_For_Additem(object):
    def setupUi(self, Dialo):
        Dialo.setObjectName("Dialo")
        Dialo.resize(542, 391)
        font = QtGui.QFont()
        font.setFamily("黑体")
        Dialo.setFont(font)
        Dialo.setSizeGripEnabled(False)
        self.lineEdit = QtWidgets.QLineEdit(Dialo)
        self.lineEdit.setGeometry(QtCore.QRect(200, 140, 251, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setPlaceholderText("Please enter the account number of the friend you want to add.")
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
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
        self.pbAdd = QtWidgets.QPushButton(Dialo)
        self.pbAdd.setGeometry(QtCore.QRect(150, 300, 251, 41))
        self.pbAdd.setDefault(True)
        self.pbAdd.setObjectName("pbAdd")
        self.label_2 = QtWidgets.QLabel(Dialo)
        self.label_2.setGeometry(QtCore.QRect(70, 150, 91, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialo)
        self.label_3.setGeometry(QtCore.QRect(70, 230, 91, 16))
        self.label_3.setObjectName("label_3")
        self.comboBox = QtWidgets.QComboBox(Dialo)
        self.comboBox.setGeometry(QtCore.QRect(200, 220, 251, 41))
        self.comboBox.setObjectName("comboBox")

        self.retranslateUi(Dialo)
        QtCore.QMetaObject.connectSlotsByName(Dialo)

    def retranslateUi(self, Dialo):
        _translate = QtCore.QCoreApplication.translate
        Dialo.setWindowTitle(_translate("Dialo", "Dialog"))
        self.lineEdit.setToolTip(_translate("Dialo", "Please enter a user account"))
        self.closeBt.setToolTip(_translate("Dialo", "Exit"))
        self.pbAdd.setText(_translate("Dialo", "Add it now"))
        self.label_2.setText(_translate("Dialo", "Contact account"))
        self.label_3.setText(_translate("Dialo", "Contact grouping"))

