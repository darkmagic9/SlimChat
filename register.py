from PyQt5.QtWidgets import QFileDialog, QWidget, QDialog, QApplication, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QEvent, QRegExp, QPoint
from PyQt5.QtGui import QKeyEvent, QKeySequence, QRegExpValidator, QPainter, QPixmap, QIcon
from PyQt5 import QtGui
import sys
from protocol import *
from Register_ui import Ui_Dialog_For_Register
class RegisterDialog(QDialog, Ui_Dialog_For_Register):
	def __init__(self, client):
		super(RegisterDialog, self).__init__()
		self.setupUi(self)
		self.client = client
		self.label.setScaledContents(True)

		self.flag = False
		self.iconpath = 'img/2-1.bmp'
		self.label.setPixmap(QPixmap(self.iconpath))
		#icon = QtGui.QIcon()
		#icon.addPixmap(QtGui.QPixmap("res/logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		self.initUI()

	def initUI(self):
		self.setWindowIcon(QIcon('img/bubbles-alt-icon.png'))
		self.scanPic.setEnabled(False)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.editPwd.setEchoMode(QLineEdit.Password)
		self.editPwd.setContextMenuPolicy(Qt.NoContextMenu)
		self.editRepPwd.setEchoMode(QLineEdit.Password)
		self.editRepPwd.setContextMenuPolicy(Qt.NoContextMenu)
		self.bcakgroundPic.installEventFilter(self)

		self.closeBt.clicked.connect(self.cancel)
		self.minBt.clicked.connect(self.showMinimized)
		self.pbLogin.clicked.connect(self.confirm)
		self.scanPic.clicked.connect(self.scanPicClicked)

		self.m_drag = False
		self.m_DragPosition = QPoint()

	def on_default_2_toggled(self, checked):
		self.flag = False
		self.label.setPixmap(QPixmap('img/2-1.bmp'))
		if self.scanPic.isEnabled() == True:
			self.scanPic.setEnabled(False)

	def on_choosePic_toggled(self, checked):
		self.flag = True
		if self.scanPic.isEnabled() == False:
			self.scanPic.setEnabled(True)

	def scanPicClicked(self):
		fname = QFileDialog.getOpenFileName(self, 'Open a file','./res/user/',("Images (*.png *.jpg *.bmp)"))
		if fname[0]:
			self.iconpath = fname[0]
			self.label.setPixmap(QPixmap(fname[0]))


	def mousePressEvent(self, event):
		if event.button()== Qt.LeftButton:
			self.m_drag=True
			self.m_DragPosition=event.globalPos()-self.pos()
			event.accept()

	def mouseMoveEvent(self, QMouseEvent):
		if QMouseEvent.buttons() and Qt.LeftButton:
			self.move(QMouseEvent.globalPos()-self.m_DragPosition)
			QMouseEvent.accept()

	def mouseReleaseEvent(self, QMouseEvent):
		self.m_drag=False

	def eventFilter(self, obj, event):
		if obj == self.bcakgroundPic:
			if event.type() == QEvent.Paint:
				painter = QPainter(self.bcakgroundPic)
				painter.drawPixmap(self.bcakgroundPic.rect(), QPixmap('img\login_register.png'))
		return QWidget.eventFilter(self, obj, event)

	def confirm(self):
		self.text1 = self.editPwd.text()
		self.text2 = self.editRepPwd.text()
		if self.text1 == self.text2:
			if len(self.text1) == 0:
				QMessageBox.warning(self, 'Warning', 'The password is empty!')
			elif len(self.text1) < 6:
				QMessageBox.warning(self, 'Warning', 'The password length is less than 6 digits!')
			else:
				if self.client.connectToServer():
					response, id = self.client.dealRegister(self.editName.text(), self.editPwd.text(), )
					if response == Type.OK:
						QMessageBox.information(self, 'Message', 'Registration Success!\nPlease remember your newly registered account :%s'%(id))
						self.client.id = id
						self.client.name = self.editName.text()
						with open(self.iconpath, 'rb') as pic:
							self.client.head = pic.read()               ##################################################################头像设置！！！！！ 
						self.client.dealSetHead()
						self.done(1) #结束对话框返回1
					else:
						QMessageBox.information(self, 'Message', 'Registration Failed!')
						self.client.close()
		else:
			QMessageBox.warning(self, 'Warning', 'The passwords entered twice are inconsistent!')


	def cancel(self):
		self.done(0) #结束对话框返回0


if __name__ == '__main__':
	app = QApplication(sys.argv)
	r = RegisterDialog()
	r.exec_()
	sys.exit(app.exec_())






