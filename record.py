from PyQt5.QtGui import QPainter, QStandardItem
from PyQt5.QtCore import QModelIndex, QAbstractItemModel
from PyQt5.QtWidgets import QStyleOptionViewItem, QStyledItemDelegate
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from chat import FeedBackListItem
from Record_ui import Ui_Form
from PyQt5.QtWidgets import QTextEdit, QLabel, QWidget, QVBoxLayout, QPushButton, QTextEdit,  QListWidget

class RecordTextEdit(QWidget, Ui_Form):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		self.closeBt.clicked.connect(self.close)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.m_drag = False
		self.m_DragPosition = QPoint()


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


	def append(self, msg):
		self.textEdit.append(msg)


