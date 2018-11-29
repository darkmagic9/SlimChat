from PyQt5.QtWidgets import QListWidgetItem,QFileDialog, QWidget, QDialog, QApplication, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QEvent, QRegExp, QPoint, QSize
from PyQt5.QtGui import QKeyEvent, QKeySequence, QRegExpValidator, QPainter, QPixmap, QIcon
from PyQt5 import QtGui
import sys
from protocol import *
from Cache_ui import Ui_Form_For_Cache
from message import Message
from chatThread import ChatThread
from chat_interface import FeedBackUI
from groupChat import GroupChat

class Cache(QWidget, Ui_Form_For_Cache):
	#showMessageSignal = pyqtSignal()
	#recviveMsgSignal = pyqtSignal(list)
	def __init__(self, parent):
		super().__init__()
		self.setupUi(self)
		self.parent = parent
		self.queue = {}
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.top.installEventFilter(self)
		self.minBt.clicked.connect(self.showMinimized)
		self.closeBt.clicked.connect(self.hide)
		self.system.itemDoubleClicked.connect(self.systemClicked)
		self.friends.itemDoubleClicked.connect(self.friendsClicked)
		self.group.itemDoubleClicked.connect(self.groupClicked)
		self.m_drag = False
		self.m_DragPosition = QPoint()


	#self.parent.grouplist格式为字典groupid：，groupname:, grouphead:,其中id作为索引
	def newGroupMsg(self, id, type, data):
		for f in self.parent.glist:
			if id == f['groupid']:
				name =f['groupname']
				head = f['grouphead']
				members = f['groupmember']

		flag = 1
		for i in range(self.group.count()):
			item = self.group.item(i)
			widget = self.group.itemWidget(item)
			if widget.id == id:
				if type == Type.GROUP_TEXT:
					widget.data.append((0, data.decode('utf-8')))
				elif type == Type.GROUP_PIC:
					widget.data.append((1, data))
				widget.count.setText(str(int(widget.count.text())+1))
				flag = 0
				break

		if flag:
			if type == Type.GROUP_TEXT:
				msg = Message(name, id, type, head, [(0, data.decode("utf-8"))], members)
			elif type == Type.GROUP_PIC:
				msg = Message(name, id, type, head, [(1, data)], members)
			newM = QListWidgetItem(self.group)
			newM.setSizeHint(QSize(self.group.width(), 61))
			self.group.setItemWidget(newM, msg)


	def groupClicked(self, item):
		#item = self.friends.currentItem()
		row = self.group.row(item)
		widget = self.group.itemWidget(item)
		self.group.takeItem(row)
		if widget.id in self.parent.groupChatWindow.keys():
			self.parent.groupChatWindow[widget.id].recvive(widget.data)
			self.parent.groupChatWindow[widget.id].show()
			#self.recviveMsgSignal.emit(widget.data)
			#self.parent.chatWindow[widget.id].chatWindow.show()
			#self.showMessageSignal.emit()
			#self.showMessageSignal.emit(id, widget.data)
		else:#还没创建过聊天窗口！
			groupChatWindow = GroupChat(self.parent.client.id, self.parent.client.head, widget.name, widget.id, widget.headPath, widget.members)
			#chatThread = ChatThread(chatWindow)
			groupChatWindow.sendGroupMsgSignal.connect(self.parent.sendGroupMsg)
			groupChatWindow.sendGroupPicSignal.connect(self.parent.sendGroupPic)

			groupChatWindow.recvive(widget.data)
			#self.recviveMsgSignal.connect(chatThread.chatWindow.recviveMsg)
			#self.showMessageSignal.connect(chatThread.chatWindow.showWindow)
			#chatThread.start()
			self.parent.groupChatWindow[widget.id] = groupChatWindow
			#self.recviveMsgSignal.emit(widget.data)
			#self.showMessageSignal.emit(widget.id, widget.data)
			#self.showMessageSignal.emit()
			groupChatWindow.show()


	def responseGroupItemClicked(self, item):
		fitem = self.parent.groups.currentItem()
		fwidget = self.parent.groups.itemWidget(fitem)
		id = int(fwidget.id.text())
		flag = 1
		for i in range(self.group.count()):
			item = self.group.item(i)
			widget = self.group.itemWidget(item)
			if widget.id == id: #如果这个好友的消息是在cache中了
				self.groupClicked(item)
				flag = 0
				break
			#在cache中没有相关的消息
		if flag:
			if int(fwidget.id.text()) in self.parent.groupChatWindow.keys():
				self.parent.groupChatWindow[int(fwidget.id.text())].show()
				#self.showMessageSignal.emit() #需要？？？？？？？？
				#self.parent.chatWindow[int(fwidget.id.text())].chatWindow.show()
				#self.showMessageSignal.emit(id, [])
			else:
				groupChatWindow = GroupChat(self.parent.client.id, self.parent.client.head, fwidget.name.text(), int(fwidget.id.text()), fwidget.headPath, fwidget.members)
				self.parent.groupChatWindow[int(fwidget.id.text())] = groupChatWindow
				#chatThread = ChatThread(chatWindow)
				groupChatWindow.sendGroupMsgSignal.connect(self.parent.sendGroupMsg)
				groupChatWindow.sendGroupPicSignal.connect(self.parent.sendGroupPic)
				#groupChatWindow.sendFileSignal.connect(self.parent.sendFile)
				#self.showMessageSignal.connect(chatThread.chatWindow.showWindow)
				#self.recviveMsgSignal.connect(chatThread.chatWindow.recviveMsg)
				groupChatWindow.show()



	def friendsClicked(self, item):
		#item = self.friends.currentItem()
		row = self.friends.row(item)
		widget = self.friends.itemWidget(item)
		self.friends.takeItem(row)
		if widget.id in self.parent.chatWindow.keys():
			self.parent.chatWindow[widget.id].recvive(widget.data)
			self.parent.chatWindow[widget.id].show()
			#self.recviveMsgSignal.emit(widget.data)
			#self.parent.chatWindow[widget.id].chatWindow.show()
			#self.showMessageSignal.emit()
			#self.showMessageSignal.emit(id, widget.data)
		else:#还没创建过聊天窗口！
			chatWindow = FeedBackUI(self.parent.client.id, self.parent.client.head, widget.name, widget.id, widget.headPath)
			#chatThread = ChatThread(chatWindow)
			chatWindow.sendMsgSignal.connect(self.parent.sendMsg)
			chatWindow.sendPicSignal.connect(self.parent.sendPic)
			chatWindow.sendFileSignal.connect(self.parent.sendFile)

			chatWindow.recvive(widget.data)
			#self.recviveMsgSignal.connect(chatThread.chatWindow.recviveMsg)
			#self.showMessageSignal.connect(chatThread.chatWindow.showWindow)
			#chatThread.start()
			self.parent.chatWindow[widget.id] = chatWindow
			#self.recviveMsgSignal.emit(widget.data)
			#self.showMessageSignal.emit(widget.id, widget.data)
			#self.showMessageSignal.emit()
			chatWindow.show()

		

		
	def responseFriendItemClicked(self, item):
		if item.parent():
			fitem = self.parent.treeWidget.currentItem()
			fwidget = self.parent.treeWidget.itemWidget(fitem, 0)
			id = int(fwidget.id.text())
			flag = 1
			for i in range(self.friends.count()):
				item = self.friends.item(i)
				widget = self.friends.itemWidget(item)
				if widget.id == id: #如果这个好友的消息是在cache中了
					self.friendsClicked(item)
					flag = 0
					break
			#在cache中没有相关的消息
			if flag:
				if int(fwidget.id.text()) in self.parent.chatWindow.keys():
					self.parent.chatWindow[int(fwidget.id.text())].show()
					#self.showMessageSignal.emit() #需要？？？？？？？？
					#self.parent.chatWindow[int(fwidget.id.text())].chatWindow.show()
					#self.showMessageSignal.emit(id, [])
				else:
					chatWindow = FeedBackUI(self.parent.client.id, self.parent.client.head, fwidget.name.text(), int(fwidget.id.text()), fwidget.headPath)
					self.parent.chatWindow[int(fwidget.id.text())] = chatWindow
					#chatThread = ChatThread(chatWindow)
					chatWindow.sendMsgSignal.connect(self.parent.sendMsg)
					chatWindow.sendPicSignal.connect(self.parent.sendPic)
					chatWindow.sendFileSignal.connect(self.parent.sendFile)
					#self.showMessageSignal.connect(chatThread.chatWindow.showWindow)
					#self.recviveMsgSignal.connect(chatThread.chatWindow.recviveMsg)
					chatWindow.show()
					
					#还需要考虑！
					#self.recviveMsgSignal.connect(chatWindow.recviveMsg)
					#chatThread.start()
					#self.parent.chatWindow[int(fwidget.id.text())] = chatThread
					#self.showMessageSignal.emit()
					#self.showMessageSignal.emit(int(fwidget.id.text()), [])
			


	#似乎没有问题
	def newFriendMsg(self, id, type, data):
		for f in self.parent.userslist:
			if id == f['userid']:
				name =f['username']
				head = f['head']

		flag = 1
		for i in range(self.friends.count()):
			item = self.friends.item(i)
			widget = self.friends.itemWidget(item)
			if widget.id == id:
				if type == Type.TEXT:
					widget.data.append((0, data.decode('utf-8')))
				elif type == Type.PIC:
					widget.data.append((1, data))
				widget.count.setText(str(int(widget.count.text())+1))
				flag = 0
				break

		if flag:
			if type == Type.TEXT:
				msg = Message(name, id, type, head, [(0, data.decode("utf-8"))])
			elif type == Type.PIC:
				msg = Message(name, id, type, head, [(1, data)])
			
			newM = QListWidgetItem(self.friends)
			newM.setSizeHint(QSize(self.friends.width(), 61))
			self.friends.setItemWidget(newM, msg)



	def systemClicked(self):
		item = self.system.currentItem()
		row = self.system.row(item)
		widget = self.system.itemWidget(item)
		self.system.takeItem(row)
		if widget.type == Type.BE_ADDED:
			self.parent.dealBeAdded(widget)
		elif widget.type == Type.RF_ADD:
			self.parent.dealRefuseAdd(widget.id)
		elif widget.type == Type.BE_DELED:
			QMessageBox.information(self, '提示', '账号为%s(%s)用户已把你删除！'%(widget.name, widget.id))
		elif widget.type == Type.GROUP_ADD_OK:
			QMessageBox.information(self, '提示', "加入群组%s成功，群号为%s"%(widget.name, widget.id))
		elif widget.type == Type.GROUP_NOEXIST:
			QMessageBox.information(self, '提示', "群组%d不存在！"%(widget.id))
		elif widget.type == Type.GROUP_CREATE_OK:
			QMessageBox.information(self, '提示', "群组创建成功，群号为%s"%(widget.id))



	def newSysMsg(self, id, type, data):
		#for f in self.parent.userslist:
		#	if id == f['userid']:
		#		name =f['username']
		name = data.split('\n'.encode('utf-8'), 1)[0].decode('utf-8')
		with open('img/系统消息.png', 'rb') as pic:
			head = pic.read()
		msg = Message(name, id, type, head, data)
		newM = QListWidgetItem(self.system)
		newM.setSizeHint(QSize(self.system.width(), 61))
		self.system.setItemWidget(newM, msg)
			


	##还需要定义点击事件!!!
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
				painter.drawPixmap(self.top.rect(), QPixmap("img/top.png"))#

		return QWidget.eventFilter(self, obj, event)

from PyQt5.QtWidgets import QApplication
import sys
if __name__ == '__main__':
	app = QApplication(sys.argv)
	b = Cache()
	b.show()
	sys.exit(app.exec_())