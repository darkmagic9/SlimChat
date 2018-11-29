import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QMessageBox, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from register import RegisterDialog
from copy_main import TIM
from client import Client
from protocol import *
class LoginDialog(QDialog):
	global client
	def __init__(self, parent=None):
		super(LoginDialog, self).__init__(parent)
		self.initUI()

	def initUI(self):
		self.setWindowTitle('登录')
		self.resize(400, 200)

		self.lblName = QLabel("账号", self)
		self.lblPwd = QLabel("密码", self)
		self.editName = QLineEdit(self)
		self.editName.setPlaceholderText('请输入您的账号')
		self.editPwd = QLineEdit(self)
		self.editPwd.setEchoMode(QLineEdit.Password)
		self.editPwd.setContextMenuPolicy(Qt.NoContextMenu)
		self.editPwd.setPlaceholderText('请输入您的密码')

		self.pbLogin = QPushButton('登录', self)
		self.pbCanel = QPushButton('取消', self)
		self.pbRegister = QPushButton('注册', self)

		self.pbLogin.clicked.connect(self.login)
		self.pbCanel.clicked.connect(self.cancel)
		self.pbRegister.clicked.connect(self.register)

		hbox1 = QHBoxLayout()
		hbox1.addWidget(self.lblName)
		hbox1.addWidget(self.editName)
		hbox2 = QHBoxLayout()
		hbox2.addWidget(self.lblPwd)
		hbox2.addWidget(self.editPwd)
		hbox3 = QHBoxLayout()
		hbox3.addWidget(self.pbLogin)
		hbox3.addWidget(self.pbRegister)
		hbox3.addWidget(self.pbCanel)

		vbox = QVBoxLayout()
		vbox.addLayout(hbox1)
		vbox.addLayout(hbox2)
		vbox.addLayout(hbox3)

		self.setLayout(vbox)


	def login(self):
		if client.connectToServer():
			respond = client.dealLogin(self.editName.text(), self.editPwd.text())
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
		self.done(0)

	def register(self):
		if client.connectToServer():
			self.close()
			reg = RegisterDialog(client)
			if reg.exec_():
				self.accept()
				pass
			else:
				client.sock.close()



def login():
	dialog = LoginDialog()
	if dialog.exec_():
		return True
	else:
		return False



if __name__ == '__main__':
	app = QApplication(sys.argv)
	client = Client()
	if login():
		tim = TIM(client)
		tim.show()
	sys.exit(app.exec_())
