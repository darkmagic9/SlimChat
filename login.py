import sys
from PyQt5.QtWidgets import QListWidgetItem, QWidget, QApplication, QDialog, QLabel, QLineEdit, QMessageBox, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QRegExp, QEvent, QPoint
from PyQt5.QtGui import QRegExpValidator, QPainter,  QIcon
from register import RegisterDialog
from main import TIM
from client import Client
from protocol import *
from Login_ui import *
from setup import *

class LoginDialog(QDialog, Ui_Dialog_For_Login):
	global client
	def __init__(self, parent=None):
		super(LoginDialog, self).__init__(parent)
		self.setFixedSize(540, 406)
		self.setupUi(self)
		self.initUI()

	def initUI(self):
		self.setWindowIcon(QIcon('img/bubbles-alt-icon.png'))
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.pbLogin.clicked.connect(self.login)
		self.pbRegister.clicked.connect(self.register)
		self.setupBt.clicked.connect(self.setUp)
		self.closeBt.clicked.connect(self.cancel)
		self.minBt.clicked.connect(self.showMinimized)
		self.backgroundPic.installEventFilter(self)
		self.m_drag = False
		self.m_DragPosition = QPoint()



	def eventFilter(self, obj, event):
		if obj == self.backgroundPic:
			if event.type() == QEvent.Paint:
				painter = QPainter(self.backgroundPic)
				painter.drawPixmap(self.backgroundPic.rect(), QPixmap('img\login_register.png'))
		return QWidget.eventFilter(self, obj, event)

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


	def login(self):
		if  len(self.editName.text()) == 0 or len(self.editPwd.text()) == 0:
			QMessageBox.critical(self, '错误', '账号或密码不能为空！请重新输入！')
		elif self.editName.text().isdigit() == False:
			QMessageBox.critical(self, '错误', '输入的账号应该是数字！请重新输入！')
		elif client.connectToServer():
			respond = client.dealLogin(int(self.editName.text()), self.editPwd.text())
			if respond == Type.OK:
				self.accept()
			elif respond == Type.FAIL:
				QMessageBox.critical(self, '错误', '密码和密码不匹配！请重新输入！')
				client.sock.close()
			elif respond == Type.REPEAT:
				client.sock.close()
				QMessageBox.critical(self, '提示', '该账户已在线上，不可多次登录同一个账号！')
			else:
				QMessageBox.critical(self, '提示', '不存在此用户！')
				client.sock.close()
			
				

	def cancel(self):
		self.close()
		self.reject()

		

	def register(self):
		self.close()
		reg = RegisterDialog(client)
		if reg.exec_():
			self.accept()


	def setUp(self):
		#self.hide()
		dialog = SetupDialog(client)
		dialog.exec_()
		#self.show()




def login():
	dialog = LoginDialog()
	dialog.show()
	if dialog.exec_():
		return True
	else:
		return False



if __name__ == '__main__':
	app = QApplication(sys.argv)
	app.setStyleSheet(open('styles/style5.qss').read())
	client = Client()
	dialog = LoginDialog()
	if dialog.exec_():
		tim = TIM(client)
		tim.show()
	else:
		sys.exit(app.quit())
	sys.exit(app.exec_())
