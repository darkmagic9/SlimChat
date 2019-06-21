from PyQt5.QtWidgets import QFileDialog, QWidget, QDialog, QApplication, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QEvent, QRegExp, QPoint
from PyQt5.QtGui import QIcon, QKeyEvent, QKeySequence, QRegExpValidator, QPainter, QPixmap, QImage
from PyQt5 import QtGui
import sys
from protocol import *
from Setinfo_ui import Ui_Dialog_For_Setinfo
class SetInfoDialog(QDialog, Ui_Dialog_For_Setinfo):
	def __init__(self, client):
		super(SetInfoDialog, self).__init__()
		self.setupUi(self)
		self.client = client
		self.initUI()

		self.iconpath = ''

		self.editName.setText = self.client.name
		image = QImage()
		image.loadFromData(self.client.head)
		self.lblhead.setPixmap(QPixmap.fromImage(image))
		#icon = QtGui.QIcon()
		#icon.addPixmap(QtGui.QPixmap("res/logo.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

		

	def initUI(self):
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.top.installEventFilter(self)
		self.closeBt.setIcon(QIcon('img/blueclose.png'))
		self.closeBt.clicked.connect(self.cancel)
		self.scanPic.clicked.connect(self.scanPicClicked)
		self.btDone.clicked.connect(self.confirm)
		self.editName.setText(self.client.name)
		self.m_drag = False
		self.m_DragPosition = QPoint()



	def scanPicClicked(self):
		fname = QFileDialog.getOpenFileName(self, 'Open a file','./res/user/',("Images (*.png *.jpg *.bmp)"))
		if fname[0]:
			self.iconpath = fname[0]
			self.lblhead.setPixmap(QPixmap(fname[0]))


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
		if obj == self.top:
			if event.type() == QEvent.Paint:
				painter = QPainter(self.top)
				painter.drawPixmap(self.top.rect(), QPixmap('img/top.png'))
		return QWidget.eventFilter(self, obj, event)

	def confirm(self):
		if len(self.editName.text()) > 0:
			self.client.name = self.editName.text()
			if self.iconpath != '':
				with open(self.iconpath, 'rb') as pic:
					self.client.head = pic.read()
			self.done(1)
		else:
			QMessageBox.information(self, 'Prompt', 'Username can not be blank!')
		


	def cancel(self):
		self.done(0) #结束对话框返回0


if __name__ == '__main__':
	app = QApplication(sys.argv)
	r = RegisterDialog()
	r.exec_()
	sys.exit(app.exec_())

