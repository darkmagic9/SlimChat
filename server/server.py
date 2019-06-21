from protocol import *
import socket
from threading import Thread 
import struct
import socket
import json
import sqlite3
import os
from Server_ui import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import playsound
BUFFERSIZE = 1024
HOST_ID = 0
TEMP_ID = -1

class ClientInfo:
	def __init__(self, id, name, sock, addr):
		self.id = id
		self.name = name
		self.addr = addr
		self.sock = sock


class Server(QWidget, Ui_Form):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
		self.addr = '127.0.0.1'
		self.port = 20000
		self.initUi()


	def initUi(self):
		self.lineEdit.setText(self.addr)
		self.lineEdit_2.setText(str(self.port))
		self.pushButton.clicked.connect(self.startServer)
		self.pushButton_2.clicked.connect(self.close)
		self.show()


	def startServer(self):
		self.textBrowser.append("Successfully start the server!\n")
		self.lineEdit.setEnabled(False)
		self.lineEdit_2.setEnabled(False)
		self.pushButton.setEnabled(False)
		self.addr = self.lineEdit.text().strip()
		self.port = int(self.lineEdit_2.text().strip())
		self.onlineClient = []
		with open('settings.txt', 'r+') as settings:
			self.canUsedId = int(settings.readline().strip())
			self.canUsedGid = int(settings.readline().strip())
		if not os.path.exists('users.db'):
			self.db = sqlite3.connect('users.db', check_same_thread=False)
			self.db.cursor().execute('''CREATE TABLE USERS (
				ID INT PRIMARY KEY NOT NULL,
				PASSWORD TEXT NOT NULL,
				NAME TEXT NOT NULL,
				GROUPANDFRIEND TEXT NOT NULL,
				HEAD BLOB,
				GROUPS TEXT NOT NULL
				);
				''')
			self.db.cursor().execute('''CREATE TABLE GROUPS(
				ID INT PRIMARY KEY NOT NULL,
				NAME TEXT NOT NULL,
				HEAD BLOB,
				MEMBERS TEXT NOT NULL
				);''')
			self.db.commit()
		else:
			self.db = sqlite3.connect('users.db', check_same_thread=False)
		self.buildSocket()



	def closeEvent(self, event):
		reply = QMessageBox.question(self, 'Prompt', 'Are you sure you want to quit the program?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if reply == QMessageBox.No:
			event.ignore()
		else:
			event.accept()


	def setupAddrAndPort(self, addr, port):
		self.addr = addr
		self.port = port 


	def buildSocket(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((self.addr, self.port))
		self.sock.listen(1000)
		self.deal = Thread(target=self.waitForConnection, args=())
		#self.waitForConnection()
		self.deal.setDaemon(True) 
		self.deal.start()

	def waitForConnection(self):
		while True:
			clientSock, clientAddr = self.sock.accept()
			self.textBrowser.append('%s : %s connect to the server.\n'%clientAddr)
			deal = Thread(target=self.dealEachClient, args=(clientSock, clientAddr))
			deal.start()

	def dealEachClient(self, sock, addr):
		try:
			while True:
				req = sock.recv(HEADER_SIZE)
				size, src_id, des_id, type = struct.unpack(HEADER_FORM, req)
				#完成
				if type == Type.LOGIN:
					if self.dealLogin(sock, size) != Type.OK:
						break
				#完成
				elif type == Type.REGISTER:
					self.dealRegister(sock, size)
				#完成
				elif type == Type.QUIT:
					self.dealQuit(sock, src_id)
					break
				#待验证
				elif type == Type.GET_GROUP_INFO:
					self.dealGetGroupInfo(sock, src_id)
				#完成
				elif type == Type.GET_SELF_NAME:
					self.dealGetSelfName(sock, src_id)
				#完成
				elif type == Type.GET_HEAD:
					self.dealGetHead(sock, size, src_id)
				#完成
				elif type == Type.SET_HEAD:
					self.dealSetHead(sock, size, src_id)
				#完成
				elif type == Type.SET_SELF_NAME:
					self.dealSetName(sock, size, src_id)
				#完成
				elif type == Type.ADD_FRIEND:
					self.dealAddFriend(sock, size, src_id, des_id)
				elif type == Type.AC_ADD:
					self.dealACAdd(sock, size, src_id, des_id)
				elif type == Type.RF_ADD:
					self.dealRFAdd(src_id, des_id)
				elif type == Type.DEL_FRIEND:
					self.dealDelFriend(src_id, des_id)
				elif type == Type.UPDATE:
					self.dealUpdate(sock, size, src_id)
				elif type == Type.TEXT:
					self.dealSendText(sock, size, src_id, des_id)
				elif type == Type.PIC:
					self.dealSendPic(sock, size, src_id, des_id)
				elif type == Type.FILE:
					self.dealSendFile(sock, size, src_id, des_id)
				elif type == Type.GROUP_TEXT:
					self.dealSendGroupMsg(sock, size, src_id, des_id)
				elif type == Type.GROUP_PIC:
					self.dealSendGroupPic(sock, size, src_id, des_id)
				elif type == Type.GET_GROUP_LIST:
					self.dealGetGroupList(sock, src_id)
				elif type == Type.GET_GROUP_NAME_HEAD:
					self.dealGetGroupNameAndHead(sock, size, src_id)
				elif type == Type.GET_GROUP_MEMBER:
					self.dealGetGroupMember(sock, size, src_id)
				elif type == Type.CREATE_GROUP:
					self.dealCreateGroup(sock, size, src_id)
				elif type == Type.JOIN_GROUP:
					self.dealJoinGroup(sock, size, src_id)
				elif type == Type.FILE_AC:
					self.dealAcceptFile(sock, size, src_id, des_id)
				elif type == Type.FILE_RF:
					self.dealRefuseFile(sock, size, src_id, des_id)
				elif type == Type.DEL_GROUP:
					self.dealDelGroup(sock, size, src_id)
		except:
			for client in self.onlineClient:
				if addr == client.addr:
					self.onlineClient.remove(client)
					break


	def dealDelGroup(self, sock, size, src_id):
		recvd_size = 0
		data = ''.encode('utf-8')
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d
		gid = int(data.decode('utf-8'))

		userG = list(self.db.cursor().execute("SELECT GROUPS FROM USERS WHERE ID=?", (src_id,)))
		userG = json.loads(userG[0][0])
		userG.remove(gid)
		userG = json.dumps(userG)
		self.db.cursor().execute("UPDATE USERS set GROUPS = ? where ID = ?", (userG, src_id))
		self.db.commit()



	def dealAcceptFile(self, sock, size, src_id, des_id):
		recvd_size = 0
		data = ''.encode('utf-8')
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d
		des_sock = self.findSock(des_id)
		protocol = Protocol(size, src_id, des_id, Type.FILE_AC)
		header = protocol.make_packet_header()
		des_sock.sendall(header +data)


	def dealRefuseFile(self, sock, size, src_id, des_id):
		recvd_size = 0
		data = ''.encode('utf-8')
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d
		des_sock = self.findSock(des_id)
		protocol = Protocol(size, src_id, des_id, Type.FILE_RF)
		header = protocol.make_packet_header()
		des_sock.sendall(header + data)




	def dealJoinGroup(self, sock, size, src_id):
		recvd_size = 0
		data = ''
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d.decode('utf-8')

		gid = int(data)

		d = list(self.db.cursor().execute("SELECT NAME, HEAD, MEMBERS FROM GROUPS WHERE ID=?", (gid,)))
		if len(d) == 0:
			protocol = Protocol(0, gid, src_id, Type.GROUP_NOEXIST)#源id为想要加入的群，但是不存在
			header = protocol.make_packet_header()
			sock.sendall(header)
		else:
			gmembers = json.loads(d[0][2])
			gmembers.append(src_id)
			gmembers = json.dumps(gmembers)
			self.db.cursor().execute("UPDATE GROUPS set MEMBERS = ? where ID = ?", (gmembers, gid))
			self.db.commit()
			userG = list(self.db.cursor().execute("SELECT GROUPS FROM USERS WHERE ID=?", (src_id,)))
			userG = json.loads(userG[0][0])
			userG.append(gid)
			userG = json.dumps(userG)
			self.db.cursor().execute("UPDATE USERS set GROUPS = ? where ID = ?", (userG, src_id))
			self.db.commit()
			data = d[0][0].encode('utf-8')+'\n'.encode('utf-8')+gmembers.encode('utf-8')+'\n'.encode('utf-8')+d[0][1]
			protocol = Protocol(len(data), gid, src_id, Type.GROUP_ADD_OK) #源id为想要加入的群
			header = protocol.make_packet_header()
			sock.sendall(header+data)




	def dealCreateGroup(self, sock, size, src_id):
		recvd_size = 0
		data = ''.encode('utf-8')
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d
		data = data.split('\n'.encode('utf-8'), 1)
		gname = data[0].decode('utf-8')
		ghead = data[1]
		gid = self.canUsedGid
		self.canUsedGid += 1

		with open("settings.txt", 'w') as settings:
			settings.write(str(self.canUsedId)+'\n')
			settings.write(str(self.canUsedGid)+'\n')

		data = gname.encode('utf-8')
		protocol = Protocol(len(data), gid, src_id, Type.GROUP_CREATE_OK)
		header = protocol.make_packet_header()
		sock.sendall(header+data)

		#写入数据库
		members = [src_id]
		members = json.dumps(members)
		self.db.cursor().execute("INSERT INTO GROUPS (ID,  NAME, HEAD, MEMBERS) VALUES (?, ?, ?, ?)", (gid, gname, ghead, members))
		self.db.commit()

		userG = list(self.db.cursor().execute("SELECT GROUPS FROM USERS WHERE ID=?", (src_id,)))
		userG = json.loads(userG[0][0])
		userG.append(gid)
		userG = json.dumps(userG)
		self.db.cursor().execute("UPDATE USERS set GROUPS = ? where ID = ?", (userG, src_id))
		self.db.commit()
		userG = list(self.db.cursor().execute("SELECT GROUPS FROM USERS WHERE ID=?", (src_id,)))


	def dealGetGroupMember(self, sock, size, src_id):
		des_id = int(sock.recv(size).decode('utf-8'))
		data = list(self.db.cursor().execute("SELECT MEMBERS FROM GROUPS WHERE ID=?", (des_id,)))
		data = data[0][0].encode('utf-8')
		protocol = Protocol(len(data), HOST_ID, src_id, Type.RET_HEAD)
		header = protocol.make_packet_header()
		sock.sendall(header+data)


	def dealGetGroupNameAndHead(self, sock, size, src_id):
		des_id = int(sock.recv(size).decode('utf-8'))
		data = list(self.db.cursor().execute("SELECT NAME, HEAD FROM GROUPS WHERE ID=?", (des_id,)))
		data = data[0][0].encode('utf-8') + '\n'.encode('utf-8') + data[0][1]
		protocol = Protocol(len(data), HOST_ID, src_id, Type.RET_HEAD)
		header = protocol.make_packet_header()
		sock.sendall(header+data)


	def dealGetGroupList(self, sock, src_id):
		info = list(self.db.cursor().execute("SELECT GROUPS FROM USERS WHERE ID=?", (src_id,)))
		info = info[0][0].encode('utf-8')
		protocol = Protocol(len(info), HOST_ID, src_id, Type.RET_GROUP_INFO)
		header = protocol.make_packet_header()
		sock.sendall(header+info)


	def dealSendGroupMsg(self, sock, size, src_id, des_id):
		text = ''.encode('utf-8')
		recvd_size = 0
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			text += d

		socks = self.findGroupSock(des_id)
		for member, des_sock in socks:
			if member != src_id:
				protocol = Protocol(size, des_id, member, Type.GROUP_TEXT)
				header = protocol.make_packet_header()
				des_sock.sendall(header + text)

	def dealSendGroupPic(self, sock, size, src_id, des_id):
		pic = ''.encode('utf-8')
		recvd_size = 0
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			pic += d

		for member, des_sock in self.findGroupSock(des_id):
			if member != src_id:
				protocol = Protocol(size, des_id, member, Type.GROUP_PIC)
				header = protocol.make_packet_header()
				des_sock.sendall(header + pic)


	def findGroupSock(self, groupid):
		res = []
		d = list(self.db.cursor().execute("SELECT MEMBERS FROM GROUPS WHERE ID=?", (groupid,)))
		members = json.loads(d[0][0])
		if len(d):
			for member in members:
				sock = self.findSock(member)
				if sock:
					res.append((member, sock))
		return res


	def findSock(self, id):
		for client in self.onlineClient:
			if id == client.id:
				return client.sock
		return None



	def dealSendFile(self, sock, size, src_id, des_id):
		file = ''.encode('utf-8')
		recvd_size = 0
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			file += d

		des_sock = self.findSock(des_id)
		protocol = Protocol(size, src_id, des_id, Type.FILE)
		header = protocol.make_packet_header()
		des_sock.sendall(header+file)


	def dealSendPic(self, sock, size, src_id, des_id):
		pic = ''.encode('utf-8')
		recvd_size = 0
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			pic += d

		des_sock = self.findSock(des_id)
		protocol = Protocol(size, src_id, des_id, Type.PIC)
		header = protocol.make_packet_header()
		des_sock.sendall(header + pic)



	def dealSendText(self, sock, size, src_id, des_id):
		text = ''.encode('utf-8')
		recvd_size = 0
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			text += d

		des_sock = self.findSock(des_id)
		protocol = Protocol(size, src_id, des_id, Type.TEXT)
		header = protocol.make_packet_header()
		des_sock.sendall(header + text)


	def dealUpdate(self, sock, size, id):
		recvd_size = 0
		info = ''
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			info += d.decode('utf-8')
		self.db.cursor().execute("UPDATE USERS set GROUPANDFRIEND = ? where ID = ?", (info, id))
		self.db.commit()


	def dealDelFriend(self, src_id, des_id):
		protocol = Protocol(0, src_id, des_id, Type.BE_DELED)
		header = protocol.make_packet_header()
		sock = self.findSock(des_id)
		sock.sendall(header)



	def dealRFAdd(self, src_id, des_id):
		protocol = Protocol(0, src_id, des_id, Type.RF_ADD)
		header = protocol.make_packet_header()
		sock = self.findSock(des_id)
		sock.sendall(header)



	def dealACAdd(self, sock, size, src_id, des_id):
		recvd_size = 0
		data = ''.encode('utf-8')
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d
		sock = self.findSock(des_id)
		protocol = Protocol(len(data), src_id, des_id, Type.AC_ADD)
		header = protocol.make_packet_header()
		sock.sendall(header+data)


	#def dealGetName(self, sock, size, ret_id):
	#	des_id = int(sock.recv(size).decode('utf-8'))
	#	data = list(self.db.cursor().execute("SELECT NAME FROM USERS WHERE ID=?", (des_id,)))
	#	data = data[0][0].encode('utf-8')
	#	protocol = Protocol(len(data), HOST_ID, ret_id, Type.RET_NAME)
	#	header = protocol.make_packet_header()
	#	sock.sendall(header+data)


	def dealAddFriend(self, sock, size, src_id, des_id):
		recvd_size = 0
		data = ''.encode('utf-8')
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d
		d = list(self.db.cursor().execute("SELECT NAME FROM USERS WHERE ID=?", (des_id,)))
		if len(d) == 0:
			protocol = Protocol(0, des_id, src_id, Type.NOEXIST)
			header = protocol.make_packet_header()
			sock.sendall(header)
		elif des_id not in [on.id for on in self.onlineClient]:
			protocol = Protocol(0, des_id, src_id, Type.OFFLINE)
			header = protocol.make_packet_header()
			sock.sendall(header)
		else:
			sock = self.findSock(des_id)
			protocol = Protocol(len(data), src_id, des_id, Type.BE_ADDED)
			header = protocol.make_packet_header()
			sock.sendall(header+data)



	def dealSetName(self, sock, size, id):
		recvd_size = 0
		name = ''
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			name += d.decode('utf-8')
		self.db.cursor().execute("UPDATE USERS set NAME = ? where ID = ?", (name, id))
		self.db.commit()




	def dealGetHead(self, sock, size, ret_id):
		des_id = int(sock.recv(size).decode('utf-8'))
		data = list(self.db.cursor().execute("SELECT HEAD FROM USERS WHERE ID=?", (des_id,)))
		data = data[0][0]
		protocol = Protocol(len(data), HOST_ID, ret_id, Type.RET_HEAD)
		header = protocol.make_packet_header()
		sock.sendall(header+data)

	


	#处理获取个人信息， 初始化
	def dealGetSelfName(self, sock, id):
		data = list(self.db.cursor().execute("SELECT NAME FROM USERS WHERE ID=?", (id,)))
		data = data[0][0].encode('utf-8')
		protocol = Protocol(len(data), HOST_ID, id, Type.RET_SELF_NAME)
		header = protocol.make_packet_header()
		sock.sendall(header+data)
		


	#未完成
	#def boardcastOnline(self, id):
	#	pass


	#未完成
	def boardcastOffline(self, id):
		pass


	#已完成
	def dealLogin(self, sock, size):
		info = sock.recv(size).decode('utf-8')
		info = json.loads(info)
		state =  self.check(info['id'], info['password'])
		if state == Type.OK:
			self.textBrowser.append('%s上线了！'%(info['id']))
			protocol = Protocol(0, HOST_ID, info['id'], state)
			header = protocol.make_packet_header()
			sock.sendall(header)
			name = self.getName(info['id'])
			client = ClientInfo(info['id'], name, sock, sock.getpeername())
			self.onlineClient.append(client)
			#self.boardcastOnline(id)
		else:
			protocol = Protocol(0, HOST_ID, TEMP_ID, state)
			header = protocol.make_packet_header()
			sock.sendall(header)
			sock.close()
		return state

	#待验证
	def dealGetGroupInfo(self, sock, id):
		info = list(self.db.cursor().execute("SELECT ID, PASSWORD, NAME, GROUPANDFRIEND FROM USERS WHERE ID=?", (id,)))
		info = json.loads(info[0][3])
		for g in info:
			for i in range(len(info[g])):
				if self.isOnline(id, info[g][i]['userid'], 0):
					info[g][i]['ishide'] = 0
				else:
					info[g][i]['ishide'] = 1

		info = json.dumps(info).encode('utf-8')
		protocol = Protocol(len(info), HOST_ID, id, Type.RET_GROUP_INFO)
		header = protocol.make_packet_header()
		sock.sendall(header+info)


		#未完成		#处理退出
	def dealQuit(self, sock, id):
		for c in self.onlineClient:
			if c.id == id:
				self.onlineClient.remove(c)
				break
		self.boardcastOffline(id)
		self.textBrowser.append('%s下线了'%id)
		sock.close()
		info = list(self.db.cursor().execute("SELECT ID, PASSWORD, NAME, GROUPANDFRIEND FROM USERS WHERE ID=?", (id,)))
		info = json.loads(info[0][3])
		for g in info:
			for i in range(len(info[g])):
				self.isOnline(id, info[g][i]['userid'], 1)


		

	def isOnline(self, id, des_id, flag):
		for i in range(len(self.onlineClient)):
			if des_id == self.onlineClient[i].id:
				if flag == 0:
					protocol = Protocol(0, id, des_id, Type.FRIEND_ONLINE)
					header = protocol.make_packet_header()
					self.onlineClient[i].sock.sendall(header)
				else:
					protocol = Protocol(0, id, des_id, Type.FRIEND_OFFLINE)
					header = protocol.make_packet_header()
					self.onlineClient[i].sock.sendall(header)
				return True
			else:
				return False

	#未完成
	def check(self, id, pwd):
		info = list(self.db.cursor().execute("SELECT ID, PASSWORD, NAME, GROUPANDFRIEND FROM USERS WHERE ID=?",(id,)))
		if len(info) == 0:
			return Type.NOEXIST
		else:
			if info[0][1] != pwd:
				return Type.FAIL
			elif id in [on.id for on in self.onlineClient]:
				return Type.REPEAT
			else:
				return Type.OK


	#完成
	def getName(self, id):
		info = list(self.db.cursor().execute("SELECT ID, PASSWORD, NAME, GROUPANDFRIEND FROM USERS WHERE ID=?",(id,)))
		return info[0][2]
		


	#未完成
	def dealRegister(self, sock, size):
		info = sock.recv(size).decode('utf-8')
		info = json.loads(info)
		id = self.canUsedId
		self.canUsedId += 1

		with open("settings.txt", 'w') as settings:
			settings.write(str(self.canUsedId)+'\n')
			settings.write(str(self.canUsedGid)+'\n')

		protocol = Protocol(0, HOST_ID, id, Type.OK)
		header = protocol.make_packet_header()
		sock.sendall(header)
	
		clientInfo = ClientInfo(id, info['name'], sock, sock.getsockname())
		self.onlineClient.append(clientInfo)

		#写入数据库
		group = {'我的好友':[]}
		group = json.dumps(group)
		g = []
		g = json.dumps(g)
		self.db.cursor().execute("INSERT INTO USERS (ID, PASSWORD, NAME, GROUPANDFRIEND, HEAD, GROUPS) VALUES (?, ?, ?, ?, ?, ?)", (id, info['password'], info['name'], group, ''.encode('utf-8'), g))
		self.db.commit()
		data = self.db.cursor().execute("SELECT GROUPS FROM USERS WHERE ID=?", (id,))
		data = list(data)


	def dealSetHead(self, sock, size, id):
		recvd_size = 0
		data = ''.encode('utf-8')
		while recvd_size != size:
			if size - recvd_size > BUFFERSIZE:
				d = sock.recv(BUFFERSIZE)
			else:
				d = sock.recv(size - recvd_size)
			recvd_size += len(d)
			data += d
		self.db.cursor().execute("UPDATE USERS set HEAD = ? where ID = ?", (data, id))
		self.db.commit()



if __name__ == "__main__":
	app = QApplication(sys.argv)
	text = Server()
	sys.exit(app.exec_())
	



