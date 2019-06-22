from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QSystemTrayIcon, QWidget, QTreeWidget, QAbstractItemView, QApplication, QTreeWidgetItem, QMenu, QAction, QInputDialog, QMessageBox, QCompleter
from PyQt5.QtCore import QSize, Qt, QVariant
from PyQt5.QtGui import QIcon, QFont, QBrush, QStandardItemModel, QColor, QPixmap, QPalette, QImage
import random
import sys
from Main_ui import Ui_Form_For_Main
from additem import Dialog_additem
from buddy import Buddy
from client import *
from protocol import *
from threading import Thread
import struct
from setinfo import SetInfoDialog
from mySystemTray import MySystemTray
from cache import Cache
from playsound import playsound
from add_Dialog import Add_Dialog
from message import Message
from listener import Listener
import time
from group import Group
from addGroup import AddGroup
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

BUFFERSIZE = 1024
class TIM(QWidget, Ui_Form_For_Main):
	grouplist = []
	userslist = []
	tmpuseritem = []
	groupInfo = {}
	chatWindow = {}
	groupChatWindow = {}
	my_groups = [] #Save my group
	glist = []#Save all information for each group

	def __init__(self, client):
		super().__init__()
		self.m_drag = False
		self.m_DragPosition = QPoint()
		self.cache = Cache(self)
		self.setupUi(self)
		self.client = client
		self.Ui_init()
		self.menuflag = 1
		self.temp = {}
		self.groupTemp = [] #New group id
		self.addTemp = []#Join the group id
		
		self.setStyleSheet(open('styles/style5.qss').read())
		self.setWindowIcon(QIcon('img/bubbles-alt-icon.png'))
		
		palette = QPalette()
		palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap('img/background/bg1.jpg')))
		self.setPalette(palette)


		
		self.setWindowFlag(Qt.FramelessWindowHint)
		self.tray = MySystemTray(self)

		self.listener = Listener(self)
		self.listener.newSysMsgSignal.connect(self.cache.newSysMsg)
		self.listener.newFriendMsgSignal.connect(self.newFriendMsg)
		self.listener.newGroupMsgSignal.connect(self.newGroupMsg)
		self.listener.successAddFriendSignal.connect(self.successAddFriend)
		self.listener.friendOfflineSignal.connect(self.dealFriendOffline)
		self.listener.friendsOnlineSignal.connect(self.dealFriendOnline)
		self.listener.noExistSignal.connect(self.noExist)
		self.listener.offlineSignal.connect(self.offline)
		self.listener.beDelSignal.connect(self.dealBeDel)
		self.listener.createGroupOkSignal.connect(self.dealCreateGroupOk)
		self.listener.addGroupOkSignal.connect(self.dealAddGroupOk)
		self.listener.start()


	def Ui_init(self):
		image = QImage()
		image.loadFromData(self.client.head)
		self.lblHead.setScaledContents(True)
		self.lblHead.setPixmap(QPixmap.fromImage(image))
		self.lblName.setText(self.client.name)
		self.lblId.setText(str(self.client.id))
		self.bt_search.setIcon(QIcon('img/search.png'))
		self.minBt.setIcon(QIcon('img/min.png'))
		self.closeBt.setIcon(QIcon('img/wclose.png'))
		self.setupBt.setIcon(QIcon('img/setting.png'))
		self.bt_adduser.setIcon(QIcon('img/add.png'))
		self.cacheBt.setIcon(QIcon('img/msg.png'))
		self.groupBt.setIcon(QIcon('img/群组.png'))
		self.faceBt.setIcon(QIcon("img/face.png"))
		self.lblIcon.setPixmap(QPixmap('img/chat.png'))
		self.tabWidget.setStyleSheet("background-color:rgba(255,255,255,0.7)")
		self.treeWidget.setStyleSheet("background-color:rgba(255,255,255,0)")
		self.groups.setStyleSheet("background-color:rgba(255,255,255,0)")
		self.groupList.setStyleSheet("background-color:rgba(255,255,255,0)")
		self.friendList.setStyleSheet("background-color:rgba(255,255,255,0)")


		self.m_model = QStandardItemModel(0, 1, self)
		m_completer = QCompleter(self.m_model, self)
		self.lineEdit.setCompleter(m_completer)

		m_completer.activated[str].connect(self.onUsernameChoosed)
		self.setupBt.clicked.connect(self.setUp)
		self.closeBt.clicked.connect(self.close)
		self.minBt.clicked.connect(self.showMinimized)
		self.cacheBt.clicked.connect(self.msgCache)
		self.groupBt.clicked.connect(self.addGroup)
		self.faceBt.clicked.connect(self.changeFace)
		self.treeWidget.currentItemChanged.connect(self.restatistic)
		self.treeWidget.itemClicked.connect(self.isclick)
		self.bt_adduser.clicked.connect(self.on_bt_adduser_clicked)
		self.bt_search.clicked.connect(self.on_bt_search_clicked)
		self.lineEdit.textChanged[str].connect(self.on_lineEdit_textChanged)
		self.treeWidget.itemDoubleClicked.connect(self.cache.responseFriendItemClicked)
		self.groups.itemDoubleClicked.connect(self.cache.responseGroupItemClicked)

		self.treeWidget.setIndentation(0)
		self.treeWidget.setColumnCount(1)
		self.treeWidget.setColumnWidth(0, 50)
		self.treeWidget.setHeaderLabels(['Friend'])
		self.treeWidget.header().hide()
		self.treeWidget.setIconSize(QSize(70, 70))
		self.treeWidget.setFocusPolicy(Qt.NoFocus)
		self.treeWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

		self.creategroup()
		self.initGroup()
		
		



	def closeWindow(self):
		if self.cache.isVisible() == True:
			self.cache.close()
		for i in self.chatWindow.keys():
			self.chatWindow[i].close()
		for i in self.groupChatWindow.keys():
			self.groupChatWindow[i].close()



	def dealCreateGroupOk(self, gid, data):
		gname = data.decode('utf-8')
		for info in self.groupTemp:
			if gname == info[0]:
				ghead = info[1]
				newG = Group(gname, gid, ghead, [self.client.id])
				item = QListWidgetItem(self.groups)
				item.setSizeHint(QSize(self.groups.width(), 61))
				self.groups.setItemWidget(item, newG)
				self.groupTemp.remove(info)
				self.my_groups.append(gid)
				groupdic = {
				'group' : item,
				'groupid' : gid,
				'groupname' : gname,
				'grouphead' : ghead,
				'groupmember' : [self.client.id]
				}
				self.glist.append(groupdic)
				break


	
	def dealAddGroupOk(self, gid, data):
		if gid in self.addTemp:
			data = data.split('\n'.encode('utf-8'), 2)
			gname = data[0].decode('utf-8')
			gmembers = json.loads(data[1].decode('utf-8'))
			ghead = data[2]
			item = QListWidgetItem(self.groups)
			item.setSizeHint(QSize(self.groups.width(), 61))
			newG = Group(gname, gid, ghead, gmembers)
			self.groups.setItemWidget(item, newG)
			self.addTemp.remove(gid)
			self.my_groups.append(gid)

			groupdic = {
				'group' : item,
				'groupid' : gid,
				'groupname' : gname,
				'grouphead' : ghead,
				'groupmember' : gmembers
			}
			self.glist.append(groupdic)




	def newGroupMsg(self, groupid, type, data):
		if groupid in self.groupChatWindow.keys() and self.groupChatWindow[groupid].isVisible():
			if(type == Type.GROUP_TEXT):
				self.groupChatWindow[groupid].recviveMsg(data.decode('utf-8'))
			else:
				self.groupChatWindow[groupid].recvivePic(data)
		else:
			self.cache.newGroupMsg(groupid, type, data)


	def newFriendMsg(self, id, type, data):
		if type == Type.FILE:
			for user in self.userslist:
				if id == user['userid']:
					name = user['username']
					break
			filename, file = data.split('\n'.encode('utf-8'), 1)
			filename = filename.decode('utf-8')
			response = QMessageBox.question(None, "Message", "Friend %s (%s) Send file %s，Would you like to accept it?"%(name ,id, filename), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
			if response == QMessageBox.Yes:
				filepath = QFileDialog.getSaveFileName(None, 'Save as', './'+filename, '')
				if filepath[0]:
					with open(filepath[0], 'wb') as f:
						f.write(file)
					self.client.dealAcceptFile(id, filename)
				else:
					self.client.dealRefuseFile(id, filename)
			else:
				self.client.dealRefuseFile(id, filename)
		elif type == Type.FILE_AC:
			for user in self.userslist:
				if id == user['userid']:
					name = user['username']
					break
			QMessageBox.information(None, 'Message', 'Friend %s (%s) Received file %s'%(name, id, data.decode('utf-8')))
		elif type == Type.FILE_RF:
			for user in self.userslist:
				if id == user['userid']:
					name = user['username']
					break
			QMessageBox.information(None, 'Message', 'Friend %s (%s) 拒绝接收文件 %s'%(name, id, data.decode('utf-8')))
		else:
			if id in self.chatWindow.keys() and self.chatWindow[id].isVisible():
				if type == Type.TEXT:
					self.chatWindow[id].recviveMsg(data.decode('utf-8'))
				elif type == Type.PIC:
					self.chatWindow[id].recvivePic(data)
			else:
				self.cache.newFriendMsg(id, type, data)

	def sendGroupMsg(self, id, text):
		self.client.dealSendGroupMsg(id, text)


	def sendGroupPic(self, id, pic):
		self.client.dealSendGroupPic(id, pic)


	def sendMsg(self, id, text):
		index = self.searchuser(id)
		if self.userslist[index]['ishide'] == 1:
			self.chatWindow[id].notOnline()
		else:
			self.client.dealSendMsg(id, text)

	def sendPic(self, id, bytes):
		index = self.searchuser(id)
		if self.userslist[index]['ishide'] == 1:
			self.chatWindow[id].notOnline()
		else:
			self.client.dealSendPic(id, bytes)

	def sendFile(self, id, filename):
		index = self.searchuser(id)
		if self.userslist[index]['ishide'] == 1:
			self.chatWindow[id].notOnline()
		else:
			self.client.dealSendFile(id, filename)



	def initGroup(self):#格式{群id:[群成员id]}?? #grouplist格式为：列表[群id]
		self.my_groups = groupInfo = self.client.dealGetGroupList()
		for groupid in groupInfo:
			groupname, grouphead = self.client.dealGetGroupNameAndHead(groupid)
			groupmember = self.client.dealGetGroupMember(groupid)
			group = QListWidgetItem(self.groups)
			group.setSizeHint(QSize(self.groups.width(), 55))
			groupdic = {
				'group' : group,
				'groupid' : groupid,
				'groupname' : groupname,
				'grouphead' : grouphead,
				'groupmember' : groupmember
			}

			g = Group(groupname, str(groupid), grouphead, groupmember)
			self.glist.append(groupdic)	
			self.groups.setItemWidget(group, g)
				


	def addGroup(self):
		addG = AddGroup(self.my_groups, self.groupTemp, self.addTemp)
		response = addG.exec_()
		if response == 1:
			gname, ghead = self.groupTemp[-1]
			self.client.dealCreateGroup(gname, ghead)
		elif response == 2:
			gid = self.addTemp[-1]
			self.client.dealJoinGroup(gid)


	def changeFace(self):
		file = QFileDialog.getOpenFileName(self, 'Select background', '.', ("Images (*.png *.jpg *.bmp)"))
		if file[0]:
			palette = QPalette()
			palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(file[0])))
			self.setPalette(palette)



	def noExist(self, id):
		QMessageBox.information(self, 'Prompt', 'There is no account number %s User!'%(id))
		for k, v in self.temp.items():
			if k == id:
				self.temp.pop(k)
				break

	def dealBeDel(self, id):
		dindex = self.searchuser(id)
		ishide = self.userslist[dindex]['ishide']
		delitem = self.userslist[dindex]['user']
		pindex = delitem.parent().indexOfChild(delitem)
		name = self.userslist[dindex]['username']
		del self.userslist[dindex]
		fathergroup = delitem.parent()
		findex = self.searchgroup(fathergroup)
		parentName = self.grouplist[findex]['groupname']
		if ishide == 1:
			self.grouplist[findex]['childishide'] -= 1
			self.grouplist[findex]['childcount'] -= 1
		else:
			self.grouplist[findex]['childcount'] -= 1
		delitem.parent().takeChild(pindex)
		for user in self.groupInfo[parentName]:
			if user['userid'] == id:
				self.groupInfo[parentName].remove(user)
				break


	def offline(self, id):
		QMessageBox.information(self, 'Prompt', 'Account number is %s Users are not online!'%(id))
		for k, v in self.temp.items():
			if k == id:
				self.temp.pop(k)
				break

	def dealRefuseAdd(self, id):
		QMessageBox.information(self, 'Prompt', 'Account number is %s User rejects your friend request!'%id)
		for k, v in self.temp.items():
			if k == id:
				self.temp.pop(k)
				break

	
	def dealFriendOnline(self, id):
		useritemindex = self.searchuser(id)
		if useritemindex is not None:
			self.userslist[useritemindex]['ishide'] = 0
			useritem = self.userslist[useritemindex]['user']
			parent = useritem.parent()
			findex = self.searchgroup(parent)
			widget = self.treeWidget.itemWidget(useritem, 0)
			widget.lblonlinestate.setPixmap(QPixmap("img/bullet_green.png"))
			self.grouplist[findex]['childishide'] -= 1
			fathergroupname = self.grouplist[findex]['groupname']
			fathergroupname += ' ' + str(self.grouplist[findex]['childcount'] - self.grouplist[findex]['childhide']) + '/' + str(self.grouplist[findex]['childcount'])
			parent.setText(0, fathergroupname)




	def dealBeAdded(self, widget):
		reply = QMessageBox.question(self, 'Friend add Prompt', '%s(%s)Add you as a friend'%(widget.name, widget.id), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
		if reply == QMessageBox.No:
			self.client.dealRefuseAdded(widget.id)
		else:
			info = ['my good friend', widget.name]
			dialog = Add_Dialog(info)
			for g in self.grouplist:
				dialog.comboBox.addItem(g['groupname'])
			dialog.exec_()

			self.client.dealAcceptAdded(widget.id)
			newitem = QTreeWidgetItem()
			newitem.setSizeHint(0, QSize(self.treeWidget.width(), 55)) 
			
			head = widget.data.split('\n'.encode('utf-8'), 1)[1]
			buddy = Buddy(info[1], str(widget.id), head, 0)
			userdic = {
					'user' : newitem,
					'username' : info[1],
					'userid' : widget.id,
					'head' : head,
					'ishide' : 0
					}

			cindex = self.searchgroup(info[0])
			group = self.grouplist[cindex]['group']
			self.grouplist[cindex]['childcount'] += 1
			self.userslist.append(userdic)
			group.addChild(newitem)
			self.treeWidget.setItemWidget(newitem, 0, buddy)
			self.treeWidget.setCurrentItem(newitem)

			user = {
			'username' : info[1],
			'userid' : widget.id,
			'ishide' : 0
			}
			self.groupInfo[info[0]].append(user)




		

	
	def dealFriendOffline(self, id):
		useritemindex = self.searchuser(id)
		if useritemindex is not None:
			self.userslist[useritemindex]['ishide'] = 1
			useritem = self.userslist[useritemindex]['user']
			parent = useritem.parent()
			findex = self.searchgroup(parent)
			widget = self.treeWidget.itemWidget(useritem, 0)
			widget.lblonlinestate.setPixmap(QPixmap('img/bullet-grey.png'))
			self.grouplist[findex]['childishide'] += 1
			fathergroupname = self.grouplist[findex]['groupname']
			fathergroupname += ' ' + str(self.grouplist[findex]['childcount'] - self.grouplist[findex]['childhide']) + '/' + str(self.grouplist[findex]['childcount'])
			parent.setText(0, fathergroupname)
			self.treeWidget.setCurrentItem(parent)





	def on_bt_adduser_clicked(self):
		des_id = [-1]
		adduser = Dialog_additem(des_id, self.temp, self.userslist, self.client.id)
		for g in self.grouplist:
			adduser.comboBox.addItem(g['groupname'])
		if adduser.exec_() == 1:
			data = self.client.name.encode('utf-8')+"\n".encode('utf-8')+self.client.head
			protocol = Protocol(len(data), self.client.id, des_id[0], Type.ADD_FRIEND)
			header = protocol.make_packet_header()
			self.client.sock.sendall(header+data)
			

	def successAddFriend(self, friend, head):
		newitem = QTreeWidgetItem()
		newitem.setSizeHint(0, QSize(self.treeWidget.width(), 55)) 
		friendName = friend['name']
		friendId = friend['id']
		ishide = friend['ishide']
		buddy = Buddy(friendName, str(friendId), head, ishide)
		userdic = {
				'user' : newitem,
				'username' : friendName,
				'userid' : friendId,
				'head' : head,
				'ishide' : ishide
				}
		for k, v in self.temp.items():
			if k == friend['id']:
				comboxinfo = self.temp.pop(k)
				break
		cindex = self.searchgroup(comboxinfo)
		group = self.grouplist[cindex]['group']
		groupname = self.grouplist[cindex]['groupname']
		self.grouplist[cindex]['childcount'] += 1
		self.userslist.append(userdic)
		group.addChild(newitem)
		self.treeWidget.setItemWidget(newitem, 0, buddy)
		self.treeWidget.setCurrentItem(newitem)

		user = {
		'username' : friendName,
		'userid' : friendId,
		'ishide' : 0 
		}
		self.groupInfo[groupname].append(user)

		



	
	def creategroup(self):
		self.groupInfo = groupInfo = self.client.dealInitGroupInfo()
		for groupname in groupInfo.keys():
			hidernum = 0
			group = QTreeWidgetItem(self.treeWidget)
			groupdic = {
				'group' : group,
				'groupname' : groupname,
				'childcount' : 0,
				'childhide' : 0
			}
			icon = self.searchIcon(groupname)
			group.setIcon(0, icon)


			for friend in groupInfo[groupname]:
				child = QTreeWidgetItem()
				child.setSizeHint(0, QSize(self.treeWidget.width(), 55))
				friendName = friend['username']
				friendId = friend['userid']
				ishide = friend['ishide']
				head = self.client.dealGetHead(friendId)
				buddy = Buddy(friendName, str(friendId), head, ishide)
				userdic = {
				'user' : child,
				'username' : friendName,
				'userid' : friendId,
				'head' : head,
				'ishide' : ishide
				}
				self.userslist.append(userdic)
				if friend['ishide'] == 1:
					hidernum += 1
					userdic['ishide'] = 1
				group.addChild(child)
				self.treeWidget.setItemWidget(child, 0, buddy)
				
			childnum = group.childCount()
			lastchildnum = childnum - hidernum
			groupdic['childcount'] = childnum
			groupdic['childishide'] = hidernum
			groupname += ' ' + str(lastchildnum) + '/' + str(childnum)
			group.setText(0, groupname)
			group.setExpanded(True)
			self.grouplist.append(groupdic)


	def createusers(self, num):
		randname = "黑子"
		randicon = QIcon(str(num)+'.jpg')
		font = QFont()
		font.setPointSize(16)
		isvip = random.randint(0, 5)
		ishider = random.randint(0, 5)
		if ishider == 1:
			randicon = QIcon(str(num)+'h.jpg')
		return randname, randicon, font, isvip, ishider

	def searchIcon(self, gpname2):
		if gpname2.find('Friend') >= 0:
			return QIcon('img/buddy.ico')
		elif gpname2.find('同事'):
			return QIcon('img/partner.ico')
		elif gpname2.find('黑名单'):
			return QIcon('img/blacklist.ico')
		else:
			return QIcon('img/defalut.ico')



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


	def onUsernameChoosed(self, name):
		self.lineEdit.setText(name)


	def on_lineEdit_textChanged(self, text):
		namelist = []
		for itm in self.userslist:
			username = itm['username']
			if username.find(text) >= 0:
				namelist.append(itm['username'])
		self.m_model.removeRows(0, self.m_model.rowCount())
	    
		for i in range(0, len(namelist)):
			self.m_model.insertRow(0)
			self.m_model.setData(self.m_model.index(0, 0), namelist[i])


	def on_bt_search_clicked(self):
		username = self.lineEdit.text()
		if len(username) > 0:
			useritemindex = self.searchuser(username)
			if useritemindex is not None:
				useritem = self.userslist[useritemindex]['user']
				self.treeWidget.setCurrentItem(useritem)
			else:
				QMessageBox.information(self, 'Message', 'This friend does not exist!')

	def closeEvent(self, event):
		reply = QMessageBox.question(self, 'Prompt', 'Are you sure you want to quit the program?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No:
			event.ignore()
		else:
			self.hide()
			self.client.dealUpdate(self.groupInfo)
			self.closeWindow()
			time.sleep(3)
			self.client.dealQuit()
			time.sleep(1)
			self.listener.terminate()
			event.accept()


	def msgCache(self):
		self.cache.show()




	
	def setUp(self):
		setup = SetInfoDialog(self.client)
		if setup.exec_() > 0:
			self.lblName.setText(self.client.name) ################################################################################需要设置头像！！！！！！！
			image = QImage()
			image.loadFromData(self.client.head)
			self.lblHead.setPixmap(QPixmap.fromImage(image))
			self.client.dealSetHead()
			self.client.dealSetName()




	def delGroup(self):
		hititem = self.groups.currentItem()
		group = self.groups.itemWidget(hititem)
		gid = int(group.id.text())
		self.client.dealDeleteGroup(gid)
		row = self.groups.row(hititem)
		self.groups.takeItem(row)




	def contextMenuEvent(self, event):
		x = QCursor.pos().x()
		y = QCursor.pos().y()
		widget = QApplication.widgetAt(x, y)
		if type(widget) == Group:
			menu = QMenu(self)
			pDeleteAct = QAction('Delete group', self.groups)
			menu.addAction(pDeleteAct)
			pDeleteAct.triggered.connect(self.delGroup)
			menu.popup(self.mapToGlobal(event.pos()))
		elif type(widget) == QWidget:
			hititem = self.treeWidget.currentItem()
			pgroupmenu = QMenu(self)
			pAddgroupAct = QAction('Add group', self.treeWidget)
			pRenameAct = QAction('Rename', self.treeWidget)
			pDeleteAct = QAction('Delete group', self.treeWidget)
			pgroupmenu.addAction(pAddgroupAct)
			pgroupmenu.addAction(pRenameAct)
			pgroupmenu.addAction(pDeleteAct)
			pAddgroupAct.triggered.connect(self.addgroup)
			pRenameAct.triggered.connect(self.renamegroup)
			if self.treeWidget.itemAbove(hititem) is None:
				pDeleteAct.setEnabled(False)
			else:
				pDeleteAct.setEnabled(True)
				pDeleteAct.triggered.connect(self.deletegroup)
			pgroupmenu.popup(self.mapToGlobal(event.pos()))

		elif type(widget) == Buddy:
			hititem = self.treeWidget.currentItem()
			root = hititem.parent()
			if root.childCount() > 0:
				pItemmenu = QMenu(self)
				pDeleteItemAct = QAction('Delete contact', pItemmenu)
				pItemmenu.addAction(pDeleteItemAct)
				pDeleteItemAct.triggered.connect(self.delete)
				if len(self.grouplist) > 1:
					pSubMenu = QMenu('Transfer contacts to', pItemmenu)
					pItemmenu.addMenu(pSubMenu)
					for item_dic in self.grouplist:
						if item_dic['group'] is not root:
							pMoveAct = QAction(item_dic['groupname'], pItemmenu)
							pSubMenu.addAction(pMoveAct)
							pMoveAct.triggered.connect(self.moveItem)
				if len(self.getListitems(self.menuflag)) == 1:
					pRenameItemAct = QAction('Setting note', pItemmenu)
					pItemmenu.addAction(pRenameItemAct)
					pRenameItemAct.triggered.connect(self.renameItem)
				if self.menuflag > 0 and root.childCount() > 1:
					pBatchAct= QAction('Batch operation within a group', pItemmenu)
					pItemmenu.addAction(pBatchAct)
					pBatchAct.triggered.connect(self.Batchoperation)
				elif self.menuflag < 0:
					pCancelBatchAct = QAction('Cancel batch operation', pItemmenu)
					pItemmenu.addAction(pCancelBatchAct)
					pCancelBatchAct.triggered.connect(self.CancelBatchoperation)

				pItemmenu.popup(self.mapToGlobal(event.pos()))


			


	def moveItem(self):
		movelist = self.getListitems(self.menuflag)
		togroupname = self.sender().text()
		mindex = self.searchgroup(togroupname)
		togroup = self.grouplist[mindex]['group']
		self.deleteItems(movelist, flag = 0)
		self.add(togroup, movelist)
		self.tmpuseritem.clear()

	def delete(self):
		delitems = self.getListitems(self.menuflag)
		self.deleteItems(delitems)
		self.tmpuseritem.clear()

	def deleteItems(self, items, flag=1):
		for delitem in items:
			delitem.setData(0, Qt.CheckStateRole, QVariant())
			pindex = delitem.parent().indexOfChild(delitem)
			dindex = self.searchuser(delitem)
			ishide = self.userslist[dindex]['ishide']
			id = self.userslist[dindex]['userid']
			if flag == 1:
				self.client.dealDelFriend(id)
				del self.userslist[dindex]

			fathergroup = delitem.parent()
			findex = self.searchgroup(fathergroup)
			parentName = self.grouplist[findex]['groupname']
			for user in self.groupInfo[parentName]:
				if user['userid'] == id:
					self.groupInfo[parentName].remove(user)
					break

			fathergroup = delitem.parent()
			findex = self.searchgroup(fathergroup)
			if ishide == 1:
				self.grouplist[findex]['childishide'] -= 1
				self.grouplist[findex]['childcount'] -= 1
			else:
				self.grouplist[findex]['childcount'] -= 1

			delitem.parent().takeChild(pindex)


	def add(self, group, items):
		gindex = self.searchgroup(group)
		gname = self.grouplist[gindex]['groupname']
		for item in items:
			aindex = self.searchuser(item)
			ishide = self.userslist[aindex]['ishide']
			userid = self.userslist[aindex]['userid']
			username = self.userslist[aindex]['username']
			head = self.userslist[aindex]['head']
			if ishide == 1:
				self.grouplist[gindex]['childishide'] += 1
				self.grouplist[gindex]['childcount'] += 1
			else:
				self.grouplist[gindex]['childcount'] += 1
			buddy = Buddy(username, str(userid), head, ishide)
			
			group.addChild(item)
			self.treeWidget.setItemWidget(item, 0, buddy)
			self.treeWidget.itemWidget(item, 0).show()
			self.treeWidget.setCurrentItem(item)

			user = {
			'username' : username,
			'userid' : userid,
			'ishide' : 0 
			}
			self.groupInfo[gname].append(user)

				



	def Batchoperation(self):
		self.menuflag *= -1
		group = self.getListitems()[0].parent()
		childnum = group.childCount()
		for c in range(childnum):
			child = group.child(c)
			child.setCheckState(0, Qt.Unchecked)

	def CancelBatchoperation(self):
		self.menuflag *= -1
		group = self.getListitems()[0].parent()
		childnum = group.childCount()
		for c in range(childnum):
			child = group.child(c)
			child.setData(0, Qt.CheckStateRole, QVariant())

	def isclick(self, item):
		if item.checkState(0) == Qt.Checked:
			if self.tmpuseritem.count(item) == 0:
				self.tmpuseritem.append(item)
		else:
			if len(self.tmpuseritem) > 0:
				if self.tmpuseritem.count(item) != 0:
					i = self.tmpuseritem.index(item)
					del self.tmpuseritem[i]

	def renameItem(self):
		hituser = self.treeWidget.currentItem()
		widget = self.treeWidget.itemWidget(hituser, 0)
		uindex = self.searchuser(hituser)
		unewname, ok = QInputDialog.getText(self, 'Prompt Information', 'Please enter a note name')
		if ok:
			if len(unewname) == 0:
				QMessageBox.information(self, 'Prompt', 'Note name cannot be empty')
			else:
				widget.name.setText(unewname)
				self.userslist[uindex]['username'] = unewname
				id = self.userslist[uindex]['userid']
				parent = hituser.parent()
				parentIndex = self.searchgroup(parent)
				parentName = self.grouplist[parentIndex]['groupname']
				for user in self.groupInfo[parentName]:
					if user['userid'] == id:
						user['username'] = unewname



	def searchuser(self, hituser):
		if isinstance(hituser, str):
			if hituser.isdigit():
				for i, u in enumerate(self.userslist):
					if str(u['userid']) == hituser:
						return i 
			else:
				for i, u in enumerate(self.userslist):
					if u['username'] == hituser :
						return i 
		elif isinstance(hituser, int):
			for i, u in enumerate(self.userslist):
				if u['userid'] == hituser:
					return i 
		else:
			for i, u in enumerate(self.userslist):
				if hituser == u['user']:
					return i
		return None



	def getListitems(self, flag=1):
		if flag > 0:
			return self.treeWidget.selectedItems()
		else:
			return self.tmpuseritem


	def addgroup(self):
		gname, ok = QInputDialog.getText(self, 'Prompt Information', 'Please enter a group name')
		if ok:
			if len(gname) == 0:
				QMessageBox.information(self, 'Prompt', 'Group name cannot be empty')
			else:
				hidernum = 0
				group = QTreeWidgetItem(self.treeWidget)
				groupdic = {
					'group' : group,
					'groupname' : gname,
					'childcount' : 0,
					'childhide' : 0
				}
				#sself.groupInfo[gname] = ''
				icon = self.searchIcon(gname)
				group.setIcon(0, icon)	
				childnum = group.childCount()
				lastchildnum = childnum - hidernum
				groupdic['childcount'] = childnum
				groupdic['childishide'] = hidernum
				self.groupInfo[gname] = []
				gname += ' ' + str(lastchildnum) + '/' + str(childnum)
				group.setText(0, gname)
				self.grouplist.append(groupdic)
				






	def renamegroup(self):
		hitgroup = self.treeWidget.currentItem()
		gnewname, ok = QInputDialog.getText(self, 'Prompt', 'Please enter a new group name')
		if ok:
			if len(gnewname) == 0:
				QMessageBox.information(self, 'Prompt', 'Group name cannot be empty')
			else:
				hitgroup.setText(0, gnewname)
				newicon = self.searchIcon(hitgroup.text(0))
				hitgroup.setIcon(0, newicon)
				gindex = self.searchgroup(hitgroup)
				oldname = self.grouplist[gindex]['groupname']
				self.grouplist[gindex]['groupname'] = gnewname
				self.treeWidget.setCurrentItem(hitgroup.child(0))
				self.groupInfo[gnewname] = self.groupInfo.pop(oldname)



	def deletegroup(self):
		hitgroup = self.treeWidget.currentItem()
		gindex = self.searchgroup(hitgroup)
		reply = QMessageBox.question(self, 'Warning', 'Are you sure you want to delete this group?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.Yes:
			self.treeWidget.takeTopLevelItem(gindex)
			groupname = self.grouplist[gindex]['groupname']
			del self.grouplist[gindex]
			del self.groupInfo[groupname]


	def searchgroup(self, hitgroup):
		if isinstance(hitgroup, str):
			for i, g in enumerate(self.grouplist):
				if g['groupname'] == hitgroup:
					return i
		else:
			for i, g in enumerate(self.grouplist):
				if g['group'] == hitgroup:
					return i



	def restatistic(self, item, preitem):
		if item:
			fathergroup = item.parent()
			if fathergroup:
				self.restatistic_op(fathergroup)
			else:
				self.restatistic_op(item)
		elif preitem.parent().childCount() == 1:
			lastgroupname = preitem.parent().text(0).split()[0] + ' 0/0'
			preitem.parent().setText(0, lastgroupname)
			self.menuflag = 1

	def restatistic_op(self, itemorgroup):
		gindex = self.searchgroup(itemorgroup)
		totalcount = self.grouplist[gindex]['childcount']
		hidecount = self.grouplist[gindex]['childishide']
		fathergroupname = self.grouplist[gindex]['groupname']
		fathergroupname += ' ' + str(totalcount - hidecount) + '/' + str(totalcount)
		itemorgroup.setText(0, fathergroupname)









from PyQt5.QtCore import QFile
from PyQt5.QtGui import QPalette
from PyQt5 import QtGui
if __name__ == '__main__':
	app = QApplication(sys.argv)
	style = open('styles/style5.qss').read()
	c = TIM()
	c.show()
	sys.exit(app.exec_())