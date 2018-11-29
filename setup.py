from PyQt5.QtWidgets import QWidget, QDialog, QApplication, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QEvent, QRegExp, QPoint
from PyQt5.QtGui import QKeyEvent, QKeySequence, QRegExpValidator, QPainter, QPixmap
import sys
from protocol import *
from Setup_ui import *
class SetupDialog(QDialog, Ui_Dialog_For_Setup):
	def __init__(self, client):
		super(SetupDialog, self).__init__()
		self.setupUi(self)
		self.initUI()
		self.client = client

	def initUI(self):
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setFixedSize(540, 406)
		self.pbCancel.clicked.connect(self.close)
		self.pbConfirm.clicked.connect(self.confirm)
		self.closeBt.clicked.connect(self.close)
		self.minBt.clicked.connect(self.showMinimized)
		self.backgroundPic.installEventFilter(self)
		self.m_drag = False
		self.m_DragPosition = QPoint()

	def confirm(self):
		self.client.host =  self.editServerIP.text()
		self.client.port = int(self.editServerPort.text())
		self.close()

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
		if obj == self.backgroundPic:
			if event.type() == QEvent.Paint:
				painter = QPainter(self.backgroundPic)
				painter.drawPixmap(self.backgroundPic.rect(), QPixmap('img\login_register.png'))
		return QWidget.eventFilter(self, obj, event)


