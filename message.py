from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox, QFileDialog
from PyQt5.QtCore import QEvent, Qt, QRect, QTime
from PyQt5.QtGui import QPalette, QPainter, QPixmap, QImage
from MsgItem_ui import Ui_Form
from protocol import *
#头像部分需要修改！！
HOST_ID = 0
class Message(QWidget, Ui_Form):

	def __init__(self, name, id, type, headPath, data, members=None):
		super().__init__()
		self.setupUi(self)
		self.initUI(name, id, type, data)
		self.headPath = headPath
		self.id = id 
		self.type = type
		self.name = name
		self.data = data
		self.head.installEventFilter(self)
		self.members = members

	def initUI(self, name, id, type, data):
		self.time.setText(QTime.currentTime().toString(Qt.DefaultLocaleLongDate))
		if type == Type.RF_ADD:
			self.name_and_id.setText("%s (%s)拒绝了添加你为好友！"%(name, id))
			self.count.setText('')
		elif type == Type.AC_ADD:
			self.name_and_id.setText("%s (%s)接受了你的好友申请！"%(name, id))
			self.count.setText('')
		elif type == Type.BE_ADDED:
			self.name_and_id.setText("%s (%s)发来添加好友请求！"%(name, id))
			self.count.setText('')
		elif type == Type.BE_DELED:
			self.name_and_id.setText("%s (%s)已把你删除！"%(name, id))
			self.count.setText('')
		elif type == Type.GROUP_CREATE_OK:
			self.name_and_id.setText("群组创建成功，群号为%s"%(id))
			self.count.setText('')
		elif type == Type.GROUP_ADD_OK:
			self.name_and_id.setText("加入群组%s成功，群号为%s"%(name, id))
			self.count.setText('')
		elif type == Type.GROUP_NOEXIST:
			self.name_and_id.setText("群组%d不存在！"%(id))
		elif type == Type.GROUP_TEXT or type == Type.GROUP_PIC:
			self.name_and_id.setText("群组 %s (%s) 有消息！"%(name, id))
			self.count.setText('1')
		elif type == Type.FILE:
			self.name_and_id.setText("好友 %s (%s) 发来文件！"%(name, id))
		else:
			self.name_and_id.setText("好友 %s (%s)发来消息！"%(name, id))
			self.count.setText('1')


	def eventFilter(self, obj, event):
		if obj == self.head:
			if event.type() == QEvent.Paint:
				painter = QPainter(self.head)
				image = QImage()
				image.loadFromData(self.headPath)
				painter.drawPixmap(self.head.rect(), QPixmap.fromImage(image))

		return QWidget.eventFilter(self, obj, event)

from PyQt5.QtWidgets import QApplication
import sys
if __name__ == '__main__':
	app = QApplication(sys.argv)
	b = Message('hah', 'dfa', 'img/2-1.bmp')
	b.show()
	sys.exit(app.exec_())