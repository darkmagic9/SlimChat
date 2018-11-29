from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QEvent, QRegExp
from PyQt5.QtGui import QKeyEvent, QKeySequence, QRegExpValidator
import sys
from protocol import *
class RegisterDialog(QDialog):
	def __init__(self, client):
		super(RegisterDialog, self).__init__()
		self.client = client
		self.initUI()

	def initUI(self):
		self.setWindowTitle('注册')
		self.resize(500, 200)

		self.lblName = QLabel('  账号  ', self)
		self.lblName.setAlignment(Qt.AlignRight)
		self.lblPwd = QLabel('  密码  ', self)
		self.lblPwd.setAlignment(Qt.AlignRight)
		self.lblRepPwd = QLabel('重复密码', self)
		self.lblRepPwd.setAlignment(Qt.AlignRight)

		self.editName = QLineEdit(self)
		self.editName.setPlaceholderText('请输入注册账号')
		self.editPwd = QLineEdit(self)
		self.editPwd.setPlaceholderText('请输入注册密码')
		self.editPwd.setEchoMode(QLineEdit.Password)
		self.editPwd.setContextMenuPolicy(Qt.NoContextMenu)
		self.editRepPwd = QLineEdit(self)
		self.editRepPwd.setPlaceholderText('请重新输入注册密码')
		self.editRepPwd.setEchoMode(QLineEdit.Password)
		self.editRepPwd.setContextMenuPolicy(Qt.NoContextMenu)

		self.pbConfirm = QPushButton('确定', self)
		self.pbCancel = QPushButton('取消', self)


		hbox1 = QHBoxLayout()
		hbox1.addWidget(self.lblName)
		hbox1.addWidget(self.editName)
		hbox2 = QHBoxLayout()
		hbox2.addWidget(self.lblPwd)
		hbox2.addWidget(self.editPwd)
		hbox3 = QHBoxLayout()
		hbox3.addWidget(self.lblRepPwd)
		hbox3.addWidget(self.editRepPwd)
		hbox4 = QHBoxLayout()
		hbox4.addWidget(self.pbConfirm)
		hbox4.addWidget(self.pbCancel)

		vbox = QVBoxLayout()
		vbox.addLayout(hbox1)
		vbox.addLayout(hbox2)
		vbox.addLayout(hbox3)
		vbox.addLayout(hbox4)

		self.setLayout(vbox)
		self.pbCancel.clicked.connect(self.cancel)
		self.pbConfirm.clicked.connect(self.confirm)

	def confirm(self):
		self.text1 = self.editPwd.text()
		self.text2 = self.editRepPwd.text()
		if self.text1 == self.text2:
			if len(self.text1) == 0:
				QMessageBox.warning(self, '警告', '密码为空!')
			elif len(self.text1) < 6:
				QMessageBox.warning(self, '警告', '密码长度低于6位！')
			else:
				response, id = self.client.dealRegister(self.editName.text(), self.editPwd.text())
				if response == Type.OK:
					QMessageBox.information(self, '消息', '注册成功！\n请记住您新注册的账号：%s'%(id))
					self.done(1) #结束对话框返回1
				else:
					QMessageBox.information(self, '消息', '注册失败！')
		else:
			QMessageBox.warning(self, '警告', '两次输入的密码不一致！')


	def cancel(self):
		self.done(0) #结束对话框返回0


if __name__ == '__main__':
	app = QApplication(sys.argv)
	r = RegisterDialog()
	r.exec_()
	sys.exit(app.exec_())






