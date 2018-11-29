# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MsgItem_ui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(493, 61)
        self.head = QtWidgets.QWidget(Form)
        self.head.setGeometry(QtCore.QRect(10, 10, 40, 40))
        self.head.setObjectName("head")
        self.name_and_id = QtWidgets.QLabel(Form)
        self.name_and_id.setGeometry(QtCore.QRect(60, 20, 271, 16))
        self.name_and_id.setText("")
        self.name_and_id.setObjectName("name_and_id")
        self.time = QtWidgets.QLabel(Form)
        self.time.setGeometry(QtCore.QRect(410, 20, 71, 20))
        self.time.setText("")
        self.time.setObjectName("time")
        self.count = QtWidgets.QLabel(Form)
        self.count.setGeometry(QtCore.QRect(341, 20, 51, 20))
        self.count.setText("")
        self.count.setObjectName("count")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

