from PyQt5.QtGui import QPainter, QStandardItem
from PyQt5.QtCore import QModelIndex, QAbstractItemModel
from PyQt5.QtWidgets import QStyleOptionViewItem, QStyledItemDelegate
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from chat import FeedBackListItem
from AddGroup_ui import Ui_Dialog_For_AddGroup
from record import RecordTextEdit
from PyQt5.QtWidgets import QTextEdit, QLabel, QWidget, QVBoxLayout, QPushButton, QTextEdit,  QListWidget

class AddGroup(QDialog, Ui_Dialog_For_AddGroup):
	def __init__(self, my_groups, groupTemp, addTemp, parent=None):
		super().__init__(parent)
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setupUi(self)

		self.scanPic.clicked.connect(self.scanPicClicked)
		self.btDone.clicked.connect(self.btDoneClicked)
		self.pbAdd.clicked.connect(self.pbAddClicked)
		self.closeBt.clicked.connect(self.cancel)

		self.m_drag = False
		self.m_DragPosition = QPoint()
		self.iconpath = ''
		with open("img/群众.png", "rb") as head:
			self.head = head.read()
		self.my_groups = my_groups
		self.groupTemp = groupTemp #[（群名， 群头像）]
		self.addTemp = addTemp#[群id的列表]


	def scanPicClicked(self):
		fname = QFileDialog.getOpenFileName(self, 'Open a file','./res/user/',("Images (*.png *.jpg *.bmp)"))
		if fname[0]:
			self.iconpath = fname[0]
			self.lblhead.setPixmap(QPixmap(fname[0]))

	#新建群组
	def btDoneClicked(self):
		if len(self.editName.text()) > 0:
			if self.iconpath != '':
				with open(self.iconpath, 'rb') as pic:
					self.head = pic.read()
			self.groupTemp.append((self.editName.text(), self.head))
			self.done(1)
		else:
			QMessageBox.information(self, 'Prompt', 'The group name cannot be empty!')


	def pbAddClicked(self):
		if len(self.editId.text()) == 0:
			QMessageBox.information(self,'Prompt','Group account is empty')
			self.editId.setFocus()
		elif self.editId.text().isdigit() == False:
			QMessageBox.critical(self, 'Prompt', 'The group account number should be a number, please re-enter!')
		else:
			if int(self.editId.text()) in self.my_groups:
				QMessageBox.information(self, 'Prompt', 'This group already exists in the group list!')
			else:
				#self.des_id[0] = int(self.lineEdit.text())
				self.addTemp.append(int(self.editId.text()))
				self.done(2)#给主窗口的返回值


	def cancel(self):
		self.done(0)


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