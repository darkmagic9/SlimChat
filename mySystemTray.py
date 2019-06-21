from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QMenu, QMessageBox, QWidget
from PyQt5.QtGui import QIcon, QCursor
#from PyQt5.QtCore import 


class MySystemTray(QSystemTrayIcon, QWidget):
	def __init__(self, parent=None):
		super(MySystemTray, self).__init__(parent)
		self.parent = parent
		self.initUi()

	def initUi(self):
		self.setIcon(QIcon('img/bubbles-alt-icon.png'))
		self.show()
		minAction = QAction("Minimize", self.parent, triggered=self.parent.showMinimized)
		openAction = QAction("Open the main panel", self.parent, triggered=self.parent.show)
		quitAction = QAction("Quit", self.parent, triggered=self.parent.close)
		setupAction = QAction("Setting", self.parent, triggered=self.parent.setUp)
		changeFaceAction = QAction("Skinning", self.parent, triggered=self.parent.changeFace)
		addFriendAction = QAction("Add friend", self.parent, triggered=self.parent.on_bt_adduser_clicked)
		cacheAction = QAction("Open message box", self.parent, triggered=self.parent.msgCache)
		groupAction = QAction("Create or join a group", self.parent, triggered=self.parent.addGroup)
		trayMenu = QMenu(self.parent) #这里的参数需要测试！
		trayMenu.addAction(minAction)
		trayMenu.addAction(openAction)
		trayMenu.addAction(quitAction)
		trayMenu.addAction(setupAction)
		trayMenu.addAction(changeFaceAction)
		trayMenu.addAction(addFriendAction)
		trayMenu.addAction(cacheAction)
		trayMenu.addAction(groupAction)
		self.setContextMenu(trayMenu)
		self.setToolTip("SlimChat\naccount number：%s\nnickname：%s\nOnline"%(self.parent.client.id, self.parent.client.name))
		self.activated.connect(self.trayClicked)
		self.showMessage("Message", 'Go online!')




	def trayClicked(self, reason):
		if reason == 3:
			self.parent.show()


