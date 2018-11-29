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
		minAction = QAction("最小化", self.parent, triggered=self.parent.showMinimized)
		openAction = QAction("打开主面板", self.parent, triggered=self.parent.show)
		quitAction = QAction("退出", self.parent, triggered=self.parent.close)
		setupAction = QAction("设置", self.parent, triggered=self.parent.setUp)
		changeFaceAction = QAction("换肤", self.parent, triggered=self.parent.changeFace)
		addFriendAction = QAction("添加好友", self.parent, triggered=self.parent.on_bt_adduser_clicked)
		cacheAction = QAction("打开消息盒子", self.parent, triggered=self.parent.msgCache)
		groupAction = QAction("新建或加入群组", self.parent, triggered=self.parent.addGroup)
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
		self.setToolTip("SlimChat\n账号：%s\n昵称：%s\n在线"%(self.parent.client.id, self.parent.client.name))
		self.activated.connect(self.trayClicked)
		self.showMessage("消息", '已上线！')




	def trayClicked(self, reason):
		if reason == 3:
			self.parent.show()


