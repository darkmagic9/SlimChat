# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GroupChat_ui1.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form_For_GroupChat(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(992, 776)
        self.m_textEdt = QtWidgets.QTextEdit(Form)
        self.m_textEdt.setGeometry(QtCore.QRect(0, 570, 771, 211))
        self.m_textEdt.setObjectName("m_textEdt")
        self.m_listWgt = QtWidgets.QListWidget(Form)
        self.m_listWgt.setGeometry(QtCore.QRect(0, 90, 771, 431))
        self.m_listWgt.setObjectName("m_listWgt")
        self.s_pic = QtWidgets.QToolButton(Form)
        self.s_pic.setGeometry(QtCore.QRect(0, 520, 51, 51))
        self.s_pic.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.s_pic.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("img/pic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.s_pic.setIcon(icon)
        self.s_pic.setAutoRaise(True)
        self.s_pic.setObjectName("s_pic")
        #self.s_file = QtWidgets.QToolButton(Form)
        #self.s_file.setGeometry(QtCore.QRect(50, 520, 51, 51))
        #self.s_file.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        #self.s_file.setText("")
        #icon1 = QtGui.QIcon()
        #icon1.addPixmap(QtGui.QPixmap("img/file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #self.s_file.setIcon(icon1)
        #self.s_file.setAutoRaise(True)
        #self.s_file.setObjectName("s_file")
        self.lblHead = QtWidgets.QLabel(Form)
        self.lblHead.setGeometry(QtCore.QRect(20, 10, 60, 60))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        self.lblHead.setFont(font)
        self.lblHead.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lblHead.setText("")
        self.lblHead.setScaledContents(True)
        self.lblHead.setObjectName("lblHead")
        self.lblName = QtWidgets.QLabel(Form)
        self.lblName.setGeometry(QtCore.QRect(110, 10, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        self.lblName.setFont(font)
        self.lblName.setText("")
        self.lblName.setObjectName("lblName")
        self.lblId = QtWidgets.QLabel(Form)
        self.lblId.setGeometry(QtCore.QRect(110, 40, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        self.lblId.setFont(font)
        self.lblId.setText("")
        self.lblId.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.lblId.setObjectName("lblId")
        self.closeBt = QtWidgets.QToolButton(Form)
        self.closeBt.setGeometry(QtCore.QRect(960, 0, 31, 31))
        self.closeBt.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("img/wclose.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeBt.setIcon(icon2)
        self.closeBt.setAutoRaise(True)
        self.closeBt.setObjectName("closeBt")

        self.minBt = QtWidgets.QToolButton(Form)
        self.minBt.setGeometry(QtCore.QRect(930, 0, 31, 31))
        self.minBt.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("img/min.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.minBt.setIcon(icon4)
        self.minBt.setAutoRaise(True)
        self.minBt.setObjectName("minBt")

        self.recordBt = QtWidgets.QToolButton(Form)
        self.recordBt.setGeometry(QtCore.QRect(710, 518, 51, 51))
        self.recordBt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.recordBt.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("img/history.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.recordBt.setIcon(icon3)
        self.recordBt.setAutoRaise(True)
        self.recordBt.setObjectName("recordBt")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(780, 60, 151, 21))
        self.label.setObjectName("label")
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setGeometry(QtCore.QRect(770, 90, 221, 691))
        self.listWidget.setObjectName("listWidget")
        self.m_submitBtn = QtWidgets.QPushButton(Form)
        self.m_submitBtn.setGeometry(QtCore.QRect(670, 730, 81, 31))
        self.m_submitBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.m_submitBtn.setObjectName("m_submitBtn")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.s_pic.setToolTip(_translate("Form", "send pictures"))
        #self.s_file.setToolTip(_translate("Form", "发送文件"))
        self.closeBt.setToolTip(_translate("Form", "Exit"))
        self.recordBt.setToolTip(_translate("Form", "View history news"))
        self.label.setText(_translate("Form", "Group member"))
        self.m_submitBtn.setText(_translate("Form", "Send"))

