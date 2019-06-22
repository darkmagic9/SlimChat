# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login_ui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QColor, QBrush, QPixmap, QIcon
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt

class Ui_Dialog_For_Login(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(540, 406)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        Dialog.setFont(font)
        Dialog.setSizeGripEnabled(False)
        self.editName = QtWidgets.QLineEdit(Dialog)
        self.editName.setGeometry(QtCore.QRect(150, 240, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.editName.setFont(font)
        self.editName.setPlaceholderText("Please enter a user account")
        self.editName.setClearButtonEnabled(False)
        self.editName.setObjectName("editName")
        self.editPwd = QtWidgets.QLineEdit(Dialog)
        self.editPwd.setGeometry(QtCore.QRect(150, 280, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        self.editPwd.setFont(font)
        self.editPwd.setPlaceholderText("Please enter a user password")
        self.editPwd.setObjectName("editPwd")
        self.pbLogin = QtWidgets.QPushButton(Dialog)
        self.pbLogin.setGeometry(QtCore.QRect(150, 340, 251, 51))
        font = QtGui.QFont()
        font.setFamily("Tahoma Light")
        font.setPointSize(13)
        self.pbLogin.setFont(font)
        self.pbLogin.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pbLogin.setObjectName("pbLogin")
        self.pbRegister = QtWidgets.QPushButton(Dialog)
        self.pbRegister.setGeometry(QtCore.QRect(440, 350, 71, 28))
        self.pbRegister.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pbRegister.setAutoDefault(True)
        self.pbRegister.setDefault(False)
        self.pbRegister.setFlat(True)
        self.pbRegister.setObjectName("pbRegister")
        self.backgroundPic = QtWidgets.QWidget(Dialog)
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
        self.setupBt = QtWidgets.QToolButton(self.backgroundPic)
        self.setupBt.setGeometry(QtCore.QRect(440, 0, 31, 41))
        self.setupBt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setupBt.setText("")
        self.setupBt.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.setupBt.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.setupBt.setAutoRaise(True)
        self.setupBt.setArrowType(QtCore.Qt.NoArrow)
        self.setupBt.setObjectName("setupBt")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        icon = QIcon()
        icon.addPixmap(QPixmap('img\setup.png'), QIcon.Normal, QIcon.Off)
        self.setupBt.setIcon(icon)
        self.editPwd.setEchoMode(QLineEdit.Password)
        self.editPwd.setContextMenuPolicy(Qt.NoContextMenu)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.editName.setToolTip(_translate("Dialog", "Please enter a user account"))
        self.editPwd.setToolTip(_translate("Dialog", "Please enter a user password"))
        self.pbLogin.setToolTip(_translate("Dialog", "Log On"))
        self.pbLogin.setText(_translate("Dialog", "Logon"))
        self.pbRegister.setToolTip(_translate("Dialog", "Registered"))
        self.pbRegister.setText(_translate("Dialog", "Registered"))
        self.closeBt.setToolTip(_translate("Dialog", "Exit"))
        self.minBt.setToolTip(_translate("Dialog", "Minimize"))
        self.setupBt.setToolTip(_translate("Dialog", "Setting"))

